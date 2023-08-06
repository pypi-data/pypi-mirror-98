import argparse
import json

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

def init_flags():
    global FLAGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="/tmp/MNIST_data",)
    parser.add_argument("--run-dir", default="/tmp/MNIST_train")
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--prepare", dest='just_data', action="store_true")
    parser.add_argument("--test", action="store_true")
    FLAGS, _ = parser.parse_known_args()

def init_data():
    global mnist
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

def init_train():
    init_model()
    init_global_step()
    init_train_op()
    init_eval_op()
    init_prediction_op()
    init_summaries()
    init_collections()
    init_session()

def init_model():
    global x, y

    # Input layer
    x = tf.placeholder(tf.float32, [None, 784])

    # First convolutional layer
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # Second convolutional layer
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # First fully connected layer
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout
    keep_prob = tf.placeholder_with_default(1.0, [])
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Output layer
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    y = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

def weight_variable(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.1))

def bias_variable(shape):
    return tf.Variable(tf.constant(0.1, shape=shape))

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding="SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(
        x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

def init_global_step():
    global global_step
    global_step = tf.Variable(0, name="global_step", trainable=False)

def init_train_op():
    global y_, loss, train_op
    y_ = tf.placeholder(tf.float32, [None, 10])
    loss = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(
            logits=y, labels=y_))
    optimizer = tf.train.AdamOptimizer(FLAGS.learning_rate)
    train_op = optimizer.minimize(loss, global_step)

def init_eval_op():
    global accuracy
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

def init_prediction_op():
    global prediction
    prediction = tf.argmax(y, 1)

def init_summaries():
    init_inputs_summary()
    init_op_summaries()
    init_summary_writers()

def init_inputs_summary():
    tf.summary.image("inputs", tf.reshape(x, [-1, 28, 28, 1]), 10)

def init_op_summaries():
    tf.summary.scalar("loss", loss)
    tf.summary.scalar("acc", accuracy)

def init_summary_writers():
    global summaries, train_writer, validate_writer
    summaries = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(
        FLAGS.run_dir,
        tf.get_default_graph())
    validate_writer = tf.summary.FileWriter(
        FLAGS.run_dir + "/val")

def init_collections():
    tf.add_to_collection("inputs", json.dumps({"image": x.name}))
    tf.add_to_collection("outputs", json.dumps({"prediction": y.name}))
    tf.add_to_collection("x", x.name)
    tf.add_to_collection("y_", y_.name)
    tf.add_to_collection("acc", accuracy.name)

def init_session():
    global sess
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

def train():
    steps = (mnist.train.num_examples // FLAGS.batch_size) * FLAGS.epochs
    for step in range(1, steps + 1):
        images, labels = mnist.train.next_batch(FLAGS.batch_size)
        batch = {x: images, y_: labels}
        sess.run(train_op, batch)
        maybe_log_accuracy(step, batch)
        maybe_checkpoint(step)

def maybe_log_accuracy(step, last_training_batch):
    epoch_step = mnist.train.num_examples / FLAGS.batch_size
    if step % 20 == 0 or step % epoch_step == 0:
        log_accuracy(last_training_batch)

def log_accuracy(last_training_batch):
    evaluate(last_training_batch, train_writer, "training")
    validate_data = {
        x: mnist.validation.images,
        y_: mnist.validation.labels
    }
    evaluate(validate_data, validate_writer, "validate")

def evaluate(data, writer, name):
    accuracy_val, summary, step = sess.run(
        [accuracy, summaries, global_step], data)
    writer.add_summary(summary, step)
    writer.flush()
    print("Step %i: %s=%f" % (step, name, accuracy_val))

def maybe_checkpoint(step):
    epoch_step = mnist.train.num_examples / FLAGS.batch_size
    if step % epoch_step == 0:
        checkpoint()

def checkpoint():
    print("Saving checkpoint")
    tf.train.Saver().save(sess, FLAGS.run_dir + "/model.ckpt", global_step)

def export_saved_model():
    print("Exporting saved model")
    builder = tf.saved_model.builder.SavedModelBuilder(
        FLAGS.run_dir + "/export")
    serve_signature = tf.saved_model.signature_def_utils.build_signature_def(
        inputs={
            "inputs": tf.saved_model.utils.build_tensor_info(x)
        },
        outputs={
            "outputs": tf.saved_model.utils.build_tensor_info(y),
            "classes": tf.saved_model.utils.build_tensor_info(prediction)
        },
        method_name="tensorflow/serving/predict"
    )
    builder.add_meta_graph_and_variables(
        sess, ["serve"],
        signature_def_map={
            "serving_default": serve_signature
        }
    )
    builder.save()

def init_test():
    init_model()
    init_global_step()
    init_train_op()
    init_eval_op()
    init_summaries()
    init_session()
    restore_latest_checkpoint()
    init_test_writer()

def restore_latest_checkpoint():
    latest_checkpoint = tf.train.latest_checkpoint(FLAGS.run_dir)
    assert latest_checkpoint, "no checkpoints in %s" % FLAGS.run_dir
    saver = tf.train.Saver()
    saver.restore(sess, latest_checkpoint)

def init_test_writer():
    global writer
    writer = tf.summary.FileWriter(FLAGS.run_dir)

def test():
    data = {x: mnist.test.images, y_: mnist.test.labels}
    test_accuracy, summary, step = sess.run(
        [accuracy, summaries, global_step],
        data)
    writer.add_summary(summary, step)
    writer.flush()
    print("Step %i: test=%f" % (step, test_accuracy))

if __name__ == "__main__":
    init_flags()
    init_data()
    if FLAGS.just_data:
        pass
    elif FLAGS.test:
        init_test()
        test()
    else:
        init_train()
        train()
        export_saved_model()
