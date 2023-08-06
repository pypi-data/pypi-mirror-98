import argparse
import json

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

def init_flags():
    global FLAGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="/tmp/MNIST_data",)
    parser.add_argument("--run-dir", default="/tmp/MNIST_train")
    parser.add_argument("--learning-rate", type=float, default=0.5)
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
    global x, y, y_, W, b
    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.nn.softmax(tf.matmul(x, W) + b)

def init_global_step():
    global global_step
    global_step = tf.Variable(0, name="global_step", trainable=False)

def init_train_op():
    global y_, loss, train_op
    y_ = tf.placeholder(tf.float32, [None, 10])
    loss = tf.reduce_mean(
             -tf.reduce_sum(
               y_ * tf.log(y),
               reduction_indices=[1]))
    optimizer = tf.train.GradientDescentOptimizer(FLAGS.learning_rate)
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
    init_variable_summaries(W, "weights")
    init_variable_summaries(b, "biases")
    init_op_summaries()
    init_summary_writers()

def init_inputs_summary():
    tf.summary.image("inputs", tf.reshape(x, [-1, 28, 28, 1]), 10)

def init_variable_summaries(var, name):
    with tf.name_scope(name):
        mean = tf.reduce_mean(var)
        tf.summary.scalar("mean", mean)
        stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar("stddev", stddev)
        tf.summary.scalar("max", tf.reduce_max(var))
        tf.summary.scalar("min", tf.reduce_min(var))
        tf.summary.histogram(name, var)

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
            "probabilities": tf.saved_model.utils.build_tensor_info(y),
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
