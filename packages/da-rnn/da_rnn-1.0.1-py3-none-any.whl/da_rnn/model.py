import tensorflow as tf
import tensorflow.keras.backend as K

from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM

from .layers import (
    EncoderInput,
    Decoder
)


class DARNN(Model):
    def __init__(
        self,
        T: int,
        m: int,
        p: int,
        y_dim: int = 1
    ):
        """
        Args:
            T (int): the size (time steps) of the window
            m (int): the number of the encoder hidden states
            p (int): the number of the decoder hidden states
            y_dim (int): prediction dimentionality

        Model Args:
            inputs: the concatenation of
            - n driving series (x_1, x_2, ..., x_T) and
            - the previous (historical) T - 1 predictions (y_1, y_2, ..., y_Tminus1, zero)

        `inputs` Explanation::

            inputs_t = (x_t__1, x_t__2, ..., x_t__n, y_t__1, y_t__2, ..., y_t__d)

            where
            - d is the prediction dimention
            - y_T__i = 0, 1 <= i <= d.

            Actually, the model will not use the value of y_T

        Usage::

            model = DARNN(10, 64, 64)
            y_hat = model(inputs)
        """

        super().__init__(name='DARNN')

        if T < 2:
            raise ValueError(
                f'T must be an integer larger than 1, but got `{T}`'
            )

        self.T = T
        self.m = m
        self.p = p
        self.y_dim = y_dim

        self.encoder_input = EncoderInput(T, m)
        self.encoder_lstm = LSTM(m, return_sequences=True)

        self.decoder = Decoder(T, m, p, y_dim=y_dim)

    # Equation 1
    def call(self, inputs):
        batch_size = K.shape(inputs)[0]

        X = inputs[:, :, :-self.y_dim]
        # -> (batch_size, T, n)

        # Y's window size is one less than X's
        # so, abandon `y_T`

        # By doing this, there are some benefits which makes it pretty easy to
        # processing datasets
        Y = inputs[:, :-1, -self.y_dim:]
        # -> (batch_size, T - 1, y_dim)

        h0 = tf.zeros((batch_size, self.m))
        s0 = tf.zeros((batch_size, self.m))

        X_tilde = self.encoder_input(
            X, h0, s0
        )

        # Equation 11
        encoder_h = self.encoder_lstm(X_tilde)

        y_hat_T = self.decoder(
            Y, encoder_h, h0, s0
        )
        # -> (batch_size, 1, y_dim)

        return y_hat_T

    def get_config(self):
        return {
            'T': self.T,
            'm': self.m,
            'p': self.p,
            'y_dim': self.y_dim
        }
