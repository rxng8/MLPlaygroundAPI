
import numpy as np

class Preprocessor:
    @staticmethod
    def get_2d_data(request) -> np.ndarray:
        """ Return a 2d numpy array from the json request

        Args:
            request ([type]): [description]

        Returns:
            np.ndarray: [description]
        """
        data = request.get_json()
        # print(f"data {np.asarray(data)}")
        return data