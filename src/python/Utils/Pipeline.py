from functools import reduce


class Functor:
    """
    A simple functor class used to construct a function call which later to be
    applied on an (any type) object.
    NOTE:
        It expects a function in the constructor and an (any type) object
        passed to the run or __call__ methods, which methods once called they
        construct and return the following function:
        func(obj, *args, **kwargs)
    NOTE:
        All the additional arguments which the function may take must be set in
        the __init__ method. If any of them are passed during run time an error
        will be raised.

    :func:
        The function to which the rest of the constructor arguments are about
        to be attached and then the newly created function will be returned.
        - The function needs to take at least one parameter since the object
        passed to the run/__call__ methods will always be put as a first
        argument to the function.

    :Example:

    def adder(a, b, *args, **kwargs):
        if args:
            print("adder args: %s" % args)
        if kwargs:
            print("adder kwargs: %s" % kwargs)
        res = a + b
        return res

    >>> x=Functor(adder, 8, 'foo', bar=True)
    >>> x(2)
    adder args: foo
    adder kwargs: {'bar': True}
    adder res: 10
    10

    >>> x
    <Pipeline.Functor instance at 0x7f319bbaeea8>


    """
    def __init__(self, func, *args, **kwargs):
        """
        The init method for class Functor
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, obj):
        """
        The call method for class Functor
        """
        return self.run(obj)

    def run(self, obj):
        return self.func(obj, *self.args, **self.kwargs)


class Pipeline:
    """
    A simple Functional Pipeline Class: applies a set of functions to an object,
    where the output of every previous function is an input to the next one
    """
    # DONE:
    #   To implement passing arguments to the functions - it will allow us to
    #   keep the object creation outside of the pipeline
    def __init__(self, funcLine=[]):
        """
        :obj: The object to be passed through the pipeline
        :funcLine: A list of functions or Functors of function + arguments (see
                   the Class definition above) that are to be applied sequentially
                   to the object.
                   - If any of the elements of 'funcLine' is a function, a direct
                   function call with the object as an argument is performed.
                   - If any of the elements of 'funcLine' is a Functor, then the
                   first argument of the Functor constructor is the function to
                   be evaluated and the object is passed as a first argument to
                   the function with all the rest of the arguments passed right
                   after it eg. the following Functor in the funcLine:

                   Functor(func, 'foo', bar=True)

                   will result in the following function call later when the
                   pipeline is executed:

                   func(obj, 'foo', bar=True)

        :Example:
            (using the adder function from above and an object of type int)

        >>> pipe = Pipeline([Functor(adder, 5),
                             Functor(adder, 6),
                             Functor(adder, 7, "extraArg"),
                             Functor(adder, 8, update=True)])

        >>> pipe.run(1)
        adder res: 6
        adder res: 12
        adder args: extraArg
        adder res: 19
        adder kwargs: {'update': True}
        adder res: 27
        """
        self.funcLine = funcLine

    def run(self, obj):
        return reduce(lambda obj, functor: functor(obj), self.funcLine, obj)
