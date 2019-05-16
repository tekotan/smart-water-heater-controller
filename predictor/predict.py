import predictor.my_model as my_model

model = my_model.get_model()
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)
