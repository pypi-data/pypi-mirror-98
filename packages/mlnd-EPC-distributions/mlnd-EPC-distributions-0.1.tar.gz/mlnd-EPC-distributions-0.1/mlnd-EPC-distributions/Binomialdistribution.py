import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        p (float) representing the probability of an event occurring
        n (int) the total number of trials

    """

    def __init__(self, prob=.5, size=20):

        self.p = prob
        self.n = size
        super().__init__(mu=self.calculate_mean(), sigma=self.calculate_stdev())

    def calculate_mean(self):

        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

        self.mean = self.p * self.n
        return self.mean

    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        self.stdev = (self.n * self.p * (1 - self.p)) ** 0.5
        return self.stdev

    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """

        self.n = len(self.data)
        self.p = sum(self.data) / self.n
        self.calculate_mean()
        self.calculate_stdev()
        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.hist(self.data)
        plt.title('Histogram of Data')
        plt.xlabel('data')
        plt.ylabel('count')

    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        return (self.p ** k) * ((1 - self.p) ** (self.n - k)) * math.factorial(self.n) / (
                math.factorial(k) * math.factorial(self.n - k))

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """

    def __add__(self, other):

        """Function to add together two Binomial mlnd-EPC-distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        p_new = self.p
        n_new = self.n + other.n
        return Binomial(prob=p_new, size=n_new)

    def __repr__(self):

        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """

        return 'mean {mu}, standard deviation {sigma}, p {prob}, n {size}'.format(
            mu=self.mean,
            sigma=self.stdev,
            prob=self.p,
            size=self.n
        )
