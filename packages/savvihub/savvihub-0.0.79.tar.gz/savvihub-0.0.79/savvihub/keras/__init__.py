import keras

from savvihub import log


class SavviHubCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        log(step=epoch, row=logs)
