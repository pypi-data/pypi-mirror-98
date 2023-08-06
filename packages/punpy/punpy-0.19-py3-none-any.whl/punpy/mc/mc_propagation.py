"""Use Monte Carlo to propagate uncertainties"""

import warnings
from multiprocessing import Pool

import numpy as np

import punpy.utilities.utilities as util

"""___Authorship___"""
__author__ = "Pieter De Vis"
__created__ = "30/03/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"


class MCPropagation:
    def __init__(self, steps, parallel_cores=0, dtype=None):
        """
        Initialise MC Propagator

        :param steps: number of MC iterations
        :type steps: int
        :param parallel_cores: number of CPU to be used in parallel processing
        :type parallel_cores: int
        """

        self.MCsteps = steps
        self.parallel_cores = parallel_cores
        self.dtype = dtype
        if parallel_cores>1:
            self.pool = Pool(self.parallel_cores)

    def propagate_random(
        self,
        func,
        x,
        u_x,
        corr_x=None,
        param_fixed=None,
        corr_between=None,
        return_corr=False,
        return_samples=False,
        repeat_dims=-99,
        corr_axis=-99,
        fixed_corr_var=False,
        output_vars=1,
        PD_corr=True,
    ):
        """
        Propagate random uncertainties through measurement function with n input quantities.
        Input quantities can be floats, vectors (1d-array) or images (2d-array).
        Random uncertainties arise when there is no correlation between repeated measurements.
        It is possible (though rare) that there is a correlation in one of the dimensions that is not one of the repeat_dims.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of random uncertainties on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param corr_x: list of correlation matrices (n,n) along non-repeating axis, defaults to None. Can optionally be set to "rand" (diagonal correlation matrix), "syst" (correlation matrix of ones) or a custom correlation matrix.
        :type corr_x: list[array], optional
        :param param_fixed: when repeat_dims>=0, set to true or false to indicate for each input quantity whether it has repeated measurements that should be split (param_fixed=False) or whether the input is fixed (param fixed=True), defaults to None (no inputs fixed).
        :type param_fixed: list of bools, optional
        :param corr_between: correlation matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to False
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :param repeat_dims: set to positive integer(s) to select the axis which has repeated measurements. The calculations will be performed seperately for each of the repeated measurments and then combined, in order to save memory and speed up the process.  Defaults to -99, for which there is no reduction in dimensionality..
        :type repeat_dims: integer or list of 2 integers, optional
        :param corr_axis: set to positive integer to select the axis used in the correlation matrix. The correlation matrix will then be averaged over other dimensions. Defaults to -99, for which the input array will be flattened and the full correlation matrix calculated.
        :type corr_axis: integer, optional
        :param fixed_corr_var: set to integer to copy the correlation matrix of the dimiension the integer refers to. Set to True to automatically detect if only one uncertainty is present and the correlation matrix of that dimension should be copied. Defaults to False.
        :type fixed_corr_var: bool or integer, optional
        :param output_vars: number of output parameters in the measurement function. Defaults to 1.
        :type output_vars: integer, optional
        :param PD_corr: set to True to make sure returned correlation matrices are positive semi-definite, default to True
        :type PD_corr: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        (
            yshapes,x,u_x,corr_x,
            n_repeats,
            repeat_shape,
            repeat_dims,
            corr_axis,
            fixed_corr,
        ) = self.perform_checks(
            func,
            x,
            u_x,
            corr_x,
            repeat_dims,
            corr_axis,
            output_vars,
            fixed_corr_var,
            param_fixed,
        )

        if n_repeats > 0:
            outs = np.empty(n_repeats, dtype=object)
            for i in range(n_repeats):
                xb, u_xb = util.select_repeated_x(
                    x, u_x, param_fixed, i, repeat_dims, repeat_shape
                )
                outs[i] = self.propagate_random(
                    func,
                    xb,
                    u_xb,
                    corr_x,
                    param_fixed,
                    corr_between,
                    return_corr,
                    return_samples,
                    -99,
                    corr_axis=corr_axis,
                    output_vars=output_vars,
                    fixed_corr_var=fixed_corr_var,
                    PD_corr=False,
                )

            return self.combine_repeated_outs(
                outs,
                yshapes,
                len(x),
                n_repeats,
                repeat_shape,
                repeat_dims,
                return_corr,
                return_samples,
                output_vars,
            )

        else:
            MC_data = np.empty(len(x), dtype=np.ndarray)
            for i in range(len(x)):
                if corr_x is None:
                    MC_data[i] = self.generate_samples_random(x[i], u_x[i])
                elif corr_x[i] is None or corr_x[i] == "rand":
                    MC_data[i] = self.generate_samples_random(x[i], u_x[i])
                elif corr_x[i] == "syst":
                    MC_data[i] = self.generate_samples_systematic(x[i], u_x[i])
                else:
                    MC_data[i] = self.generate_samples_correlated(x, u_x, corr_x, i)

            if corr_between is not None:
                MC_data = self.correlate_samples_corr(MC_data, corr_between)

            return self.process_samples(
                func,
                MC_data,
                return_corr,
                return_samples,
                yshapes,
                corr_axis,
                fixed_corr,
                PD_corr,
                output_vars,
            )

    def propagate_systematic(
        self,
        func,
        x,
        u_x,
        corr_x=None,
        param_fixed=None,
        corr_between=None,
        return_corr=False,
        return_samples=False,
        repeat_dims=-99,
        corr_axis=-99,
        fixed_corr_var=False,
        output_vars=1,
        PD_corr=True,
    ):
        """
        Propagate systematic uncertainties through measurement function with n input quantities.
        Input quantities can be floats, vectors (1d-array) or images (2d-array).
        Systematic uncertainties arise when there is full correlation between repeated measurements.
        There is a often also a correlation between measurements along the dimensions that is not one of the repeat_dims.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of systematic uncertainties on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param corr_x: list of correlation matrices (n,n) along non-repeating axis, defaults to None. Can optionally be set to "rand" (diagonal correlation matrix), "syst" (correlation matrix of ones) or a custom correlation matrix.
        :type corr_x: list[array], optional
        :param param_fixed: when repeat_dims>=0, set to true or false to indicate for each input quantity whether it has repeated measurements that should be split (param_fixed=False) or whether the input is fixed (param fixed=True), defaults to None (no inputs fixed).
        :type param_fixed: list of bools, optional
        :param corr_between: correlation matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to False
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :param repeat_dims: set to positive integer(s) to select the axis which has repeated measurements. The calculations will be performed seperately for each of the repeated measurments and then combined, in order to save memory and speed up the process.  Defaults to -99, for which there is no reduction in dimensionality..
        :type repeat_dims: integer or list of 2 integers, optional
        :param corr_axis: set to positive integer to select the axis used in the correlation matrix. The correlation matrix will then be averaged over other dimensions. Defaults to -99, for which the input array will be flattened and the full correlation matrix calculated.
        :type corr_axis: integer, optional
        :param fixed_corr_var: set to integer to copy the correlation matrix of the dimiension the integer refers to. Set to True to automatically detect if only one uncertainty is present and the correlation matrix of that dimension should be copied. Defaults to False.
        :type fixed_corr_var: bool or integer, optional
        :param output_vars: number of output parameters in the measurement function. Defaults to 1.
        :type output_vars: integer, optional
        :param PD_corr: set to True to make sure returned correlation matrices are positive semi-definite, default to True
        :type PD_corr: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        (
            yshapes,
            x,
            u_x,
            corr_x,
            n_repeats,
            repeat_shape,
            repeat_dims,
            corr_axis,
            fixed_corr,
        ) = self.perform_checks(
            func,
            x,
            u_x,
            corr_x,
            repeat_dims,
            corr_axis,
            output_vars,
            fixed_corr_var,
            param_fixed,
        )

        if n_repeats > 0:
            outs = np.empty(n_repeats, dtype=object)
            for i in range(n_repeats):
                xb, u_xb = util.select_repeated_x(
                    x, u_x, param_fixed, i, repeat_dims, repeat_shape
                )

                outs[i] = self.propagate_systematic(
                    func,
                    xb,
                    u_xb,
                    corr_x,
                    param_fixed,
                    corr_between,
                    return_corr,
                    return_samples,
                    -99,
                    corr_axis=corr_axis,
                    fixed_corr_var=fixed_corr_var,
                    output_vars=output_vars,
                    PD_corr=False,
                )

            return self.combine_repeated_outs(
                outs,
                yshapes,
                len(x),
                n_repeats,
                repeat_shape,
                repeat_dims,
                return_corr,
                return_samples,
                output_vars,
            )

        else:
            MC_data = np.empty(len(x), dtype=np.ndarray)
            for i in range(len(x)):
                if corr_x is None:
                    MC_data[i] = self.generate_samples_systematic(x[i], u_x[i])
                elif corr_x[i] is None or corr_x[i] == "syst":
                    MC_data[i] = self.generate_samples_systematic(x[i], u_x[i])
                elif corr_x[i] == "rand":
                    MC_data[i] = self.generate_samples_random(x[i], u_x[i])
                else:
                    MC_data[i] = self.generate_samples_correlated(x, u_x, corr_x, i)

            if corr_between is not None:
                MC_data = self.correlate_samples_corr(MC_data, corr_between)

            return self.process_samples(
                func,
                MC_data,
                return_corr,
                return_samples,
                yshapes,
                corr_axis,
                fixed_corr,
                PD_corr,
                output_vars,
            )

    def propagate_cov(
        self,
        func,
        x,
        cov_x,
        param_fixed=None,
        corr_between=None,
        return_corr=True,
        return_samples=False,
        repeat_dims=-99,
        corr_axis=-99,
        fixed_corr_var=False,
        output_vars=1,
        PD_corr=True,
    ):
        """
        Propagate uncertainties with given covariance matrix through measurement function with n input quantities.
        Input quantities can be floats, vectors (1d-array) or images (2d-array).
        The covariance matrix can represent the full covariance matrix between all measurements in all dimensions.
        Alternatively if there are repeated measurements specified in repeat_dims, the covariance matrix is given
        for the covariance along the dimension that is not one of the repeat_dims.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param cov_x: list of covariance matrices on input quantities (usually numpy arrays). In case the input quantity is an array of shape (m,o), the covariance matrix needs to be given as an array of shape (m*o,m*o).
        :type cov_x: list[array]
        :param param_fixed: when repeat_dims>=0, set to true or false to indicate for each input quantity whether it has repeated measurements that should be split (param_fixed=False) or whether the input is fixed (param fixed=True), defaults to None (no inputs fixed).
        :type param_fixed: list of bools, optional
        :param corr_between: covariance matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to True
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :param repeat_dims: set to positive integer(s) to select the axis which has repeated measurements. The calculations will be performed seperately for each of the repeated measurments and then combined, in order to save memory and speed up the process.  Defaults to -99, for which there is no reduction in dimensionality..
        :type repeat_dims: integer or list of 2 integers, optional
        :param corr_axis: set to positive integer to select the axis used in the correlation matrix. The correlation matrix will then be averaged over other dimensions. Defaults to -99, for which the input array will be flattened and the full correlation matrix calculated.
        :type corr_axis: integer, optional
        :param fixed_corr_var: set to integer to copy the correlation matrix of the dimiension the integer refers to. Set to True to automatically detect if only one uncertainty is present and the correlation matrix of that dimension should be copied. Defaults to False.
        :type fixed_corr_var: bool or integer, optional
        :param output_vars: number of output parameters in the measurement function. Defaults to 1.
        :type output_vars: integer, optional
        :param PD_corr: set to True to make sure returned correlation matrices are positive semi-definite, default to True
        :type PD_corr: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        (
            yshapes,x,u_x,corr_x,
            n_repeats,
            repeat_shape,
            repeat_dims,
            corr_axis,
            fixed_corr,
        ) = self.perform_checks(
            func,
            x,
            cov_x,
            None,
            repeat_dims,
            corr_axis,
            output_vars,
            fixed_corr_var,
            param_fixed,
        )

        if n_repeats > 0:
            outs = np.empty(n_repeats, dtype=object)
            for i in range(n_repeats):
                xb, _ = util.select_repeated_x(
                    x, x, param_fixed, i, repeat_dims, repeat_shape
                )
                outs[i] = self.propagate_cov(
                    func,
                    xb,
                    cov_x,
                    param_fixed,
                    corr_between,
                    return_corr,
                    return_samples,
                    -99,
                    corr_axis=corr_axis,
                    output_vars=output_vars,
                    PD_corr=False,
                )

            return self.combine_repeated_outs(
                outs,
                yshapes,
                len(x),
                n_repeats,
                repeat_shape,
                repeat_dims,
                return_corr,
                return_samples,
                output_vars,
            )

        else:
            MC_data = np.empty(len(x), dtype=np.ndarray)
            for i in range(len(x)):
                if not hasattr(x[i], "__len__"):
                    MC_data[i] = self.generate_samples_systematic(x[i], cov_x[i])
                elif all(
                    (cov_x[i] == 0).flatten()
                ):  # This is the case if one of the variables has no uncertainty
                    MC_data[i] = np.tile(x[i].flatten(), (self.MCsteps, 1)).T
                elif param_fixed is not None:
                    if param_fixed[i] and (len(x[i].shape) == 2):
                        MC_data[i] = np.array(
                            [
                                self.generate_samples_cov(
                                    x[i][:, j].flatten(), cov_x[i]
                                ).reshape(x[i][:, j].shape + (self.MCsteps,))
                                for j in range(x[i].shape[1])
                            ]
                        ).T
                        MC_data[i] = np.moveaxis(MC_data[i], 0, 1)
                    else:
                        MC_data[i] = self.generate_samples_cov(
                            x[i].flatten(), cov_x[i]
                        ).reshape(x[i].shape + (self.MCsteps,))
                else:
                    MC_data[i] = self.generate_samples_cov(
                        x[i].flatten(), cov_x[i]
                    ).reshape(x[i].shape + (self.MCsteps,))

            if corr_between is not None:
                MC_data = self.correlate_samples_corr(MC_data, corr_between)

        return self.process_samples(
            func,
            MC_data,
            return_corr,
            return_samples,
            yshapes,
            corr_axis,
            fixed_corr,
            PD_corr,
            output_vars,
        )

    def perform_checks(
        self,
        func,
        x,
        u_x,
        corr_x,
        repeat_dims,
        corr_axis,
        output_vars,
        fixed_corr_var,
        param_fixed,
    ):
        """
        Perform checks on the input parameters and set up the appropriate keywords for further processing

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of uncertainties/covariances on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param corr_x: list of correlation matrices (n,n) along non-repeating axis, defaults to None. Can optionally be set to "rand" (diagonal correlation matrix), "syst" (correlation matrix of ones) or a custom correlation matrix.
        :type corr_x: list[array], optional
        :param repeat_dims: set to positive integer(s) to select the axis which has repeated measurements. The calculations will be performed seperately for each of the repeated measurments and then combined, in order to save memory and speed up the process.  Defaults to -99, for which there is no reduction in dimensionality..
        :type repeat_dims: integer or list of 2 integers, optional
        :param corr_axis: set to positive integer to select the axis used in the correlation matrix. The correlation matrix will then be averaged over other dimensions. Defaults to -99, for which the input array will be flattened and the full correlation matrix calculated.
        :type corr_axis: integer, optional
        :param output_vars: number of output parameters in the measurement function. Defaults to 1.
        :type output_vars: integer, optional
        :param fixed_corr_var: set to integer to copy the correlation matrix of the dimiension the integer refers to. Set to True to automatically detect if only one uncertainty is present and the correlation matrix of that dimension should be copied. Defaults to False.
        :type fixed_corr_var: bool or integer, optional
        :param param_fixed: when repeat_dims>=0, set to true or false to indicate for each input quantity whether it has repeated measurements that should be split (param_fixed=False) or whether the input is fixed (param fixed=True), defaults to None (no inputs fixed).
        :type param_fixed: list of bools, optional
        :return: yshape,u_x,repeat_axis,repeat_dims,corr_axis,fixed_corr
        :rtype: tuple, list[array], int, int, int, array
        """

        # Set up repeat_axis and repeat_dims for proper use in recursive function.
        if isinstance(repeat_dims,int):
            repeat_dims = [repeat_dims]

        # find the shape
        if output_vars == 1:
            yshape = np.array(func(*x)).shape
            yshapes = [np.array(func(*x)).shape]
        else:
            yshape = np.array(func(*x)[0]).shape
            yshapes = [np.array(func(*x)[i]).shape for i in range(output_vars)]

        shapewarning = False
        for i in range(len(x)):
            if hasattr(x[i], "__len__"):
                if param_fixed is not None:
                    if (
                        x[i].shape != yshape
                        and self.parallel_cores == 0
                        and not param_fixed[i]
                    ):
                        shapewarning = True
                else:
                    if x[i].shape != yshape and self.parallel_cores == 0:
                        shapewarning = True
            else:
                if self.dtype is not None:
                    x[i]=np.array(x[i],dtype=self.dtype)
                if self.parallel_cores == 0:
                    shapewarning = True

        if shapewarning:
            warnings.warn(
                "It looks like one of your input quantities is not an array or does not "
                "have the same shape as the measurand. This is not a problem, but means "
                "you likely cannot use array operations in your measurement function. "
                "You might need to set parallel_cores to 1 or higher when creating "
                "your MCPropagation object."
            )

        # Check for which input quantities there is no uncertainty,
        # replacing Nones with zeros where necessary.
        # Count the number of non-zero uncertainties. If this number is one, the
        # correlation matrix for the measurand will be the same as for this input qty.

        count = 0
        for i in range(len(x)):
            if u_x[i] is None:
                if hasattr(x[i], "__len__"):
                    u_x[i] = np.zeros(x[i].shape)
                else:
                    u_x[i] = 0.0

            if u_x is not None:
                if u_x[i] is not None:
                    if self.dtype is not None:
                        u_x[i] = np.array(u_x[i],dtype=self.dtype)

            if corr_x is not None:
                if corr_x[i] is not None:
                    if self.dtype is not None:
                        corr_x[i]= np.array(corr_x[i],dtype=self.dtype)

            if np.sum(u_x[i]) != 0 and fixed_corr_var == True:
                count += 1
                var = i
            if corr_x is not None:
                if corr_x[i] is not None:
                    if not isinstance(corr_x[i], str):
                        if np.any(corr_x[i] > 1.000001):
                            raise ValueError(
                                "One of the provided correlation matrices "
                                "has elements >1."
                            )

        if count == 1:
            fixed_corr_var = var
        else:
            fixed_corr_var = -99

        if fixed_corr_var >= 0 and corr_x is not None:
            if corr_x[fixed_corr_var] == "rand":
                fixed_corr = np.eye(len(u_x[fixed_corr_var]))
            elif corr_x[fixed_corr_var] == "syst":
                fixed_corr = np.ones(
                    (len(u_x[fixed_corr_var]), len(u_x[fixed_corr_var]))
                )
            else:
                fixed_corr = corr_x[fixed_corr_var]

        else:
            fixed_corr = None



        if len(repeat_dims) == 1:
            if repeat_dims[0] >= 0:
                n_repeats = yshape[repeat_dims[0]]
                if corr_axis > repeat_dims[0]:
                    corr_axis -= 1
                elif corr_axis == repeat_dims[0]:
                    print("corr_axis and repeat_axis keywords should not be the same.")
                    exit()
            else:
                n_repeats = 0
            repeat_shape = (n_repeats,)  # repeat_dims = -99
        else:
            repeat_dims = -np.sort(-np.array(repeat_dims))
            n_repeats = yshape[repeat_dims[0]] * yshape[repeat_dims[1]]
            repeat_shape = (yshape[repeat_dims[0]], yshape[repeat_dims[1]])
            if corr_axis > repeat_dims[0]:
                corr_axis -= 1
            elif corr_axis == repeat_dims[0]:
                print("corr_axis and repeat_axis keywords should not be the same.")
                exit()
            if corr_axis > repeat_dims[1]:
                corr_axis -= 1
            elif corr_axis == repeat_dims[1]:
                print("corr_axis and repeat_axis keywords should not be the same.")
                exit()

        return yshapes, x, u_x, corr_x, n_repeats, repeat_shape, repeat_dims, corr_axis, fixed_corr

    def combine_repeated_outs(
        self,
        outs,
        yshapes,
        lenx,
        n_repeats,
        repeat_shape,
        repeat_dims,
        return_corr,
        return_samples,
        output_vars,
    ):
        """
        Combine the outputs of the repeated measurements into one results array

        :param outs: list of outputs of the repeated measurements
        :type outs: list[array]
        :param yshapes: shape of the measurand
        :type yshapes: tuple
        :param lenx: number of input quantities
        :type lenx: int
        :param n_repeats: number of repeated measurements
        :type n_repeats: int
        :param repeat_shape: shape along which the measurements are repeated
        :type repeat_shape: tuple
        :param repeat_dims: set to positive integer(s) to select the axis which has repeated measurements. The calculations will be performed seperately for each of the repeated measurments and then combined, in order to save memory and speed up the process.  Defaults to -99, for which there is no reduction in dimensionality..
        :type repeat_dims: integer or list of 2 integers, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to True
        :type return_corr: bool, optional
        :param return_Jacobian: set to True to return Jacobian, defaults to False
        :type return_Jacobian: bool, optional
        :param output_vars: number of output parameters in the measurement function. Defaults to 1.
        :type output_vars: integer, optional
        :return: combined outputs
        :rtype: list[array]
        """
        if not return_corr and output_vars == 1 and not return_samples:
            u_func = np.array([outs[i] for i in range(n_repeats)])

        elif output_vars == 1:
            u_func = np.array([outs[i][0] for i in range(n_repeats)])

        elif output_vars > 1 and not return_corr and not return_samples:
            u_func = np.array(
                [[outs[i][ii] for i in range(n_repeats)] for ii in range(output_vars)]
            )

        else:
            u_func = np.array(
                [
                    [outs[i][0][ii] for i in range(n_repeats)]
                    for ii in range(output_vars)
                ]
            )

        if len(repeat_dims) == 1:
            if output_vars == 1:
                u_func = np.moveaxis(u_func, 0, repeat_dims[0])
            else:
                if all([yshapes[i] == yshapes[0] for i in range(len(yshapes))]):
                    u_func = np.moveaxis(u_func, 1, repeat_dims[0] + 1)
                else:
                    u_funcb = u_func[:]
                    u_func = np.empty(output_vars, dtype=object)
                    for i in range(output_vars):
                        u_func[i] = np.empty(yshapes[i])
                        if len(yshapes[i]) == 0:
                            u_func[i] = u_funcb[i]
                        elif len(yshapes[i]) == 1:
                            for ii in range(yshapes[i][0]):
                                u_func[i][ii] = u_funcb[i][ii]
                        elif len(yshapes[i]) == 2:
                            for ii in range(yshapes[i][0]):
                                for iii in range(yshapes[i][1]):
                                    u_func[i][ii, iii] = u_funcb[i][iii][ii]
                        else:
                            print("this shape is not supported")

        else:
            if output_vars == 1:
                u_func = u_func.reshape(repeat_shape + (-1,))
                u_func = np.moveaxis(u_func, 0, repeat_dims[0])
                u_func = np.moveaxis(u_func, 0, repeat_dims[1])
            else:
                u_func = u_func.reshape((output_vars,) + repeat_shape + (-1,))
                u_func = np.moveaxis(u_func, 1, repeat_dims[0] + 1)
                u_func = np.moveaxis(u_func, 1, repeat_dims[1] + 1)

        if (output_vars == 1 and u_func.shape != yshapes[0]) or (
            output_vars > 1 and u_func[0].shape != yshapes[0]
        ):
            print(u_func.shape, yshapes[0])
            raise ValueError(
                "The shape of the uncertainties does not match the shape"
                "of the measurand. This is likely a problem with combining"
                "repeated measurements (repeat_dims keyword)."
            )

        if not return_corr and not return_samples:
            return u_func

        else:
            returns = np.empty(len(outs[0]), dtype=object)
            returns[0] = u_func
            extra_index = 0
            if return_corr:
                corr = np.mean([outs[i][1] for i in range(n_repeats)], axis=0)
                if all([yshapes[i] == yshapes[0] for i in range(len(yshapes))]):
                    if output_vars > 1:
                        for j in range(output_vars):
                            if not util.isPD(corr[j]):
                                corr[j] = util.nearestPD_cholesky(
                                    corr[j], corr=True, return_cholesky=False
                                )
                    else:
                        if not util.isPD(corr):
                            corr = util.nearestPD_cholesky(
                                corr, corr=True, return_cholesky=False
                            )

                returns[1] = corr
                extra_index += 1

            if output_vars > 1:
                if all([yshapes[i] == yshapes[0] for i in range(len(yshapes))]):
                    corr_out = np.mean(
                        [outs[i][1 + extra_index] for i in range(n_repeats)], axis=0
                    )
                    if not util.isPD(corr_out):
                        corr_out = util.nearestPD_cholesky(
                            corr_out, corr=True, return_cholesky=False
                        )
                else:
                    corr_out = None
                returns[1 + extra_index] = corr_out
                extra_index += 1

            if return_samples:
                returns[1 + extra_index] = [
                    np.vstack([outs[i][1 + extra_index][k] for i in range(n_repeats)])
                    for k in range(lenx)
                ]
                returns[2 + extra_index] = [
                    np.vstack([outs[i][2 + extra_index][k] for i in range(n_repeats)])
                    for k in range(lenx)
                ]

            return returns

    def process_samples(
        self,
        func,
        data,
        return_corr,
        return_samples,
        yshapes,
        corr_axis=-99,
        fixed_corr=None,
        PD_corr=True,
        output_vars=1,
    ):
        """
        Run the MC-generated samples of input quantities through the measurement function and calculate
        correlation matrix if required.

        :param func: measurement function
        :type func: function
        :param data: MC-generated samples of input quantities
        :type data: array[array]
        :param return_corr: set to True to return correlation matrix of measurand
        :type return_corr: bool
        :param return_samples: set to True to return generated samples
        :type return_samples: bool
        :param corr_axis: set to positive integer to select the axis used in the correlation matrix. The correlation matrix will then be averaged over other dimensions. Defaults to -99, for which the input array will be flattened and the full correlation matrix calculated.
        :type corr_axis: integer, optional
        :param fixed_corr: correlation matrix to be copied without changing, defaults to None (correlation matrix is calculated rather than copied)
        :type fixed_corr: array
        :param PD_corr: set to True to make sure returned correlation matrices are positive semi-definite, default to True
        :type PD_corr: bool, optional
        :param output_vars: number of output parameters in the measurement function. Defaults to 1.
        :type output_vars: integer, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        if self.parallel_cores == 0:
            MC_y = np.array(func(*data))

        elif self.parallel_cores == 1:
            # In order to Process the MC iterations separately, the array with the input quantities has to be reordered
            # so that it has the same length (i.e. the first dimension) as the number of MCsteps.
            # First we move the axis with the same length as self.MCsteps from the last dimension to the fist dimension
            if self.dtype is not None:
                data2 = [np.moveaxis(dat, -1, 0).astype(self.dtype) for dat in data]
            else:
                data2 = [np.moveaxis(dat, -1, 0) for dat in data]

            if output_vars == 1 or all(
                [yshapes[i] == yshapes[0] for i in range(len(yshapes))]
            ):
                # The function can then be applied to each of these MCsteps
                MC_y2 = np.array(list(map(func, *data2)))

                # We then reorder to bring it back to the original shape
                MC_y = np.moveaxis(MC_y2, 0, -1)

            else:
                MC_y = np.empty(output_vars, dtype=object)
                MC_y2 = np.array(list(map(func, *data2)))

                for i in range(output_vars):
                    MC_y[i] = np.empty(yshapes[i] + (self.MCsteps,))
                    if len(yshapes[i]) == 0:
                        for j in range(self.MCsteps):
                            MC_y[i][j] = MC_y2[j, i]
                    elif len(yshapes[i]) == 1:
                        for ii in range(yshapes[i][0]):
                            for j in range(self.MCsteps):
                                MC_y[i][ii, j] = MC_y2[j, i][ii]
                    elif len(yshapes[i]) == 2:
                        for ii in range(yshapes[i][0]):
                            for iii in range(yshapes[i][1]):
                                for j in range(self.MCsteps):
                                    MC_y[i][ii, iii, j] = MC_y2[j, i][ii, iii]
                    else:
                        print("this shape is not supported")

        else:
            # We again need to reorder the input quantities samples in order to be able to pass them to p.starmap
            # We here use lists to iterate over and order them slightly different as the case above.
            if self.dtype is not None:
                data2 = np.empty(self.MCsteps,dtype=object)
                for i in range(self.MCsteps):
                    data2[i] = [data[j][...,i] for j in range(len(data))]
            else:
                data2=np.empty(self.MCsteps)
                for i in range(self.MCsteps):
                    data2[i] = [data[j][..., i] for j in range(len(data))]
            MC_y2 = np.array(self.pool.starmap(func, data2), dtype=self.dtype)
            if output_vars == 1:
                MC_y = np.moveaxis(MC_y2, 0, -1)
            else:
                MC_y = np.empty(output_vars, dtype=object)
                for i in range(output_vars):
                    MC_y[i] = np.moveaxis(MC_y2[i], 0, -1)

        # if hasattr(MC_y[0,0], '__len__'):
        #     print(yshape,np.array(MC_y[0,0]).shape,np.array(MC_y[1,0]).shape,np.array(MC_y[2,0]).shape,np.array(MC_y[3,0]).shape)
        if output_vars == 1:
            u_func = np.std(MC_y, axis=-1)
        else:
            u_func = np.empty(output_vars, dtype=object)
            for i in range(output_vars):
                u_func[i] = np.std(np.array(MC_y[i]), axis=-1)
        if not return_corr:
            if return_samples:
                return u_func, MC_y, data
            else:
                return u_func
        else:
            if output_vars == 1:
                if fixed_corr is None:
                    corr_y = self.calculate_corr(MC_y, corr_axis).astype("float32")
                    if PD_corr:
                        if not util.isPD(corr_y):
                            corr_y = util.nearestPD_cholesky(
                                corr_y, corr=True, return_cholesky=False
                            )
                else:
                    corr_y = fixed_corr
                if return_samples:
                    return u_func, corr_y, MC_y, data
                else:
                    return u_func, corr_y

            else:
                # create an empty arrays and then populate it with the correlation matrix for each output parameter individually
                corr_ys = np.empty(output_vars, dtype=object)
                for i in range(output_vars):
                    if fixed_corr is None:
                        corr_ys[i] = self.calculate_corr(MC_y[i], corr_axis).astype(
                            "float32"
                        )
                        if PD_corr:
                            if not util.isPD(corr_ys[i]):
                                corr_ys[i] = util.nearestPD_cholesky(
                                    corr_ys[i], corr=True, return_cholesky=False
                                )
                    else:
                        corr_ys[i] = fixed_corr
                # calculate correlation matrix between the different outputs produced by the measurement function.
                if all([yshapes[i] == yshapes[0] for i in range(len(yshapes))]):
                    corr_out = np.corrcoef(MC_y.reshape((output_vars, -1))).astype(
                        "float32"
                    )
                else:
                    corr_out = None  # np.corrcoef([[np.mean(MC_y[i][:,j]) for j in range(self.MCsteps)] for i in range(output_vars)]).astype(
                    # "float32")

                if PD_corr:
                    if not util.isPD(corr_out):
                        corr_out = util.nearestPD_cholesky(
                            corr_out, corr=True, return_cholesky=False
                        )
                if return_samples:
                    return u_func, corr_ys, corr_out, MC_y, data
                else:
                    return u_func, corr_ys, corr_out

    def calculate_corr(self, MC_y, corr_axis=-99):
        """
        Calculate the correlation matrix between the MC-generated samples of output quantities.
        If corr_axis is specified, this axis will be the one used to calculate the correlation matrix (e.g. if corr_axis=0 and x.shape[0]=n, the correlation matrix will have shape (n,n)).
        This will be done for each combination of parameters in the other dimensions and the resulting correlation matrices are averaged.

        :param MC_y: MC-generated samples of the output quantities (measurands)
        :type MC_y: array
        :param corr_axis: set to positive integer to select the axis used in the correlation matrix. The correlation matrix will then be averaged over other dimensions. Defaults to -99, for which the input array will be flattened and the full correlation matrix calculated.
        :type corr_axis: integer, optional
        :return: correlation matrix
        :rtype: array
        """
        # print("the shape is:",MC_y.shape)

        if len(MC_y.shape) < 3:
            corr_y = np.corrcoef(MC_y)

        elif len(MC_y.shape) == 3:
            if corr_axis == 0:
                corr_ys = np.empty(len(MC_y[0]), dtype=object)
                for i in range(len(MC_y[0])):
                    corr_ys[i] = np.corrcoef(MC_y[:, i])
                corr_y = np.mean(corr_ys, axis=0)

            elif corr_axis == 1:
                corr_ys = np.empty(len(MC_y), dtype=object)
                for i in range(len(MC_y)):
                    corr_ys[i] = np.corrcoef(MC_y[i])
                corr_y = np.mean(corr_ys, axis=0)

            else:
                MC_y = MC_y.reshape((MC_y.shape[0] * MC_y.shape[1], self.MCsteps))
                corr_y = np.corrcoef(MC_y)

        elif len(MC_y.shape) == 4:
            if corr_axis == 0:
                corr_ys = np.empty(len(MC_y[0]) * len(MC_y[0, 0]), dtype=object)
                for i in range(len(MC_y[0])):
                    for j in range(len(MC_y[0, 0])):
                        corr_ys[i + j * len(MC_y[0])] = np.corrcoef(MC_y[:, i, j])
                corr_y = np.mean(corr_ys, axis=0)

            elif corr_axis == 1:
                corr_ys = np.empty(len(MC_y) * len(MC_y[0, 0]), dtype=object)
                for i in range(len(MC_y)):
                    for j in range(len(MC_y[0, 0])):
                        corr_ys[i + j * len(MC_y)] = np.corrcoef(MC_y[i, :, j])
                corr_y = np.mean(corr_ys, axis=0)

            elif corr_axis == 2:
                corr_ys = np.empty(len(MC_y) * len(MC_y[0]), dtype=object)
                for i in range(len(MC_y)):
                    for j in range(len(MC_y[0])):
                        corr_ys[i + j * len(MC_y)] = np.corrcoef(MC_y[i, j])
                corr_y = np.mean(corr_ys, axis=0)
            else:
                MC_y = MC_y.reshape(
                    (MC_y.shape[0] * MC_y.shape[1] * MC_y.shape[2], self.MCsteps)
                )
                corr_y = np.corrcoef(MC_y)
        else:
            print(
                "MC_y has too high dimensions. Reduce the dimensionality of the input data"
            )
            exit()

        return corr_y

    def generate_samples_correlated(self, x, u_x, corr_x, i):
        """
        Generate correlated MC samples of input quantity with given uncertainties and correlation matrix.
        Samples are generated using generate_samples_cov() after matching up the uncertainties to the right correlation matrix.
        It is possible to provide one correlation matrix to be used for each measurement (which each have an uncertainty) or a correlation matrix per measurement.

        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of uncertainties/covariances on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param corr_x: list of correlation matrices (n,n) along non-repeating axis, or list of correlation matrices for each repeated measurement.
        :type corr_x: list[array], optional
        :param i: index of the input quantity (in x)
        :type i: int
        :return: generated samples
        :rtype: array
        """
        if len(x[i].shape) == 2:
            if len(corr_x[i]) == len(u_x[i]):
                MC_data = np.zeros((u_x[i].shape) + (self.MCsteps,))
                for j in range(len(u_x[i][0])):
                    cov_x = util.convert_corr_to_cov(corr_x[i], u_x[i][:, j])
                    MC_data[:, j, :] = self.generate_samples_cov(
                        x[i][:, j].flatten(), cov_x
                    ).reshape(x[i][:, j].shape + (self.MCsteps,))
            else:
                MC_data = np.zeros((u_x[i].shape) + (self.MCsteps,))
                for j in range(len(u_x[i][:, 0])):
                    cov_x = util.convert_corr_to_cov(corr_x[i], u_x[i][j])
                    MC_data[j, :, :] = self.generate_samples_cov(
                        x[i][j].flatten(), cov_x
                    ).reshape(x[i][j].shape + (self.MCsteps,))
        else:
            cov_x = util.convert_corr_to_cov(corr_x[i], u_x[i])
            MC_data = self.generate_samples_cov(x[i].flatten(), cov_x).reshape(
                x[i].shape + (self.MCsteps,)
            )

        return MC_data

    def generate_samples_random(self, param, u_param):
        """
        Generate MC samples of input quantity with random (Gaussian) uncertainties.

        :param param: values of input quantity (mean of distribution)
        :type param: float or array
        :param u_param: uncertainties on input quantity (std of distribution)
        :type u_param: float or array
        :return: generated samples
        :rtype: array
        """
        if not hasattr(param, "__len__"):
            return np.random.normal(size=self.MCsteps).astype(self.dtype) * u_param + param
        elif len(param.shape) ==0:
            return np.random.normal(size=self.MCsteps).astype(self.dtype) * u_param + param
        elif len(param.shape) == 1:
            return (
                np.random.normal(size=(len(param), self.MCsteps)).astype(self.dtype) * u_param[:, None]
                + param[:, None]
            )
        elif len(param.shape) == 2:
            return (
                np.random.normal(size=param.shape + (self.MCsteps,))
                * u_param[:, :, None]
                + param[:, :, None]
            )
        elif len(param.shape) == 3:
            return (
                np.random.normal(size=param.shape + (self.MCsteps,)).astype(self.dtype)
                * u_param[:, :, :, None]
                + param[:, :, :, None]
            )
        else:
            print("parameter shape not supported: ", param.shape, param)
            exit()

    def generate_samples_systematic(self, param, u_param):
        """
        Generate correlated MC samples of input quantity with systematic (Gaussian) uncertainties.

        :param param: values of input quantity (mean of distribution)
        :type param: float or array
        :param u_param: uncertainties on input quantity (std of distribution)
        :type u_param: float or array
        :return: generated samples
        :rtype: array
        """
        if not hasattr(param, "__len__"):
            return np.random.normal(size=self.MCsteps).astype(self.dtype) * u_param + param
        elif len(param.shape) ==0:
            return np.random.normal(size=self.MCsteps).astype(self.dtype) * u_param + param
        elif len(param.shape) == 1:
            return (
                np.dot(u_param[:, None], np.random.normal(size=self.MCsteps).astype(self.dtype)[None, :])
                + param[:, None]
            )
        elif len(param.shape) == 2:
            return (
                np.dot(
                    u_param[:, :, None],
                    np.random.normal(size=self.MCsteps).astype(self.dtype)[:, None, None],
                )[:, :, :, 0]
                + param[:, :, None]
            )
        elif len(param.shape) == 3:
            return (
                np.dot(
                    u_param[:, :, :, None],
                    np.random.normal(size=self.MCsteps).astype(self.dtype)[:, None, None, None],
                )[:, :, :, :, 0, 0]
                + param[:, :, :, None]
            )
        else:
            print("parameter shape not supported")
            exit()

    def generate_samples_cov(self, param, cov_param):
        """
        Generate correlated MC samples of input quantity with a given covariance matrix.
        Samples are generated independent and then correlated using Cholesky decomposition.

        :param param: values of input quantity (mean of distribution)
        :type param: array
        :param cov_param: covariance matrix for input quantity
        :type cov_param: array
        :return: generated samples
        :rtype: array
        """
        try:
            L = np.linalg.cholesky(cov_param)
        except:
            L = util.nearestPD_cholesky(cov_param)

        return (
            np.dot(L, np.random.normal(size=(len(param), self.MCsteps)).astype(self.dtype))
            + param[:, None]
        )

    def correlate_samples_corr(self, samples, corr):
        """
        Method to correlate independent samples of input quantities using correlation matrix and Cholesky decomposition.

        :param samples: independent samples of input quantities
        :type samples: array[array]
        :param corr: correlation matrix between input quantities
        :type corr: array
        :return: correlated samples of input quantities
        :rtype: array[array]
        """
        if np.max(corr) > 1.000001 or len(corr) != len(samples):
            raise ValueError(
                "The correlation matrix between variables is not the right shape or has elements >1."
            )
        else:
            try:
                L = np.array(np.linalg.cholesky(corr))
            except:
                L = util.nearestPD_cholesky(corr)

            # Cholesky needs to be applied to Gaussian distributions with mean=0 and std=1,
            # We first calculate the mean and std for each input quantity
            means = np.array([np.mean(samples[i]) for i in range(len(samples))],dtype=self.dtype)
            stds = np.array([np.std(samples[i]) for i in range(len(samples))],dtype=self.dtype)

            # We normalise the samples with the mean and std, then apply Cholesky, and finally reapply the mean and std.
            if all(stds != 0):
                return np.dot(L, (samples - means) / stds) * stds + means

            # If any of the variables has no uncertainty, the normalisation will fail. Instead we leave the parameters without uncertainty unchanged.
            else:
                samples_out = samples[:]
                id_nonzero = np.where(stds != 0)
                samples_out[id_nonzero] = (
                    np.dot(
                        L[id_nonzero][:, id_nonzero],
                        (samples[id_nonzero] - means[id_nonzero]) / stds[id_nonzero],
                    )[:, 0]
                    * stds[id_nonzero]
                    + means[id_nonzero]
                )
                return samples_out
