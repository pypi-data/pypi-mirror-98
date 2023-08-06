# latticetools

Numpy and Matplotlib are great tools to model systems numerically and throw together quick plots, as well as highly specific, complex plots too. For example, a 2D distribution in $X$ and $Y$:


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
X, Y = np.ogrid[:100,:100]
func = ((X - 50) * (1 / 50) **.5) ** 2 + (Y - 50)
```


```python
plt.imshow(func, extent = (0, 100, 100, 0))
plt.colorbar()
plt.xlabel('Y')
plt.ylabel('X')
plt.show()
```


![jpeg](latticetools-intro/output_4_0.jpg)


It's not too hard to describe the distribution and plot it with a few lines of code. However, there can be situations where even this process can become repetitive and slow down work. For example, making small changes to the distribution and plotting again — this might require copying the plotting code lines or re-running the lines again in-place:


```python
func2 = abs(func) ** .5
```


```python
plt.imshow(func2, extent = (0, 100, 100, 0))
plt.colorbar()
plt.xlabel('Y')
plt.ylabel('X')
plt.show()
```


![jpeg](latticetools-intro/output_7_0.jpg)


This makes for a potentially cluttered and non-linear work process. latticetools was developed to streamline this procedure, both in terms of generating distributions and particularly in visually representing them.


```python
import latticetools
```

latticetools is a module that centralises the definition of a sampled n-dimensional space and takes care of all the details which depend on the sampling. Be it a 1-dimensional time-series or 3D volume of data, latticetools can be used to set-and-forget the sample spacing and limits of the data. latticetools's features include:
* Easy production of consistent plots and imshows of 1D and 2D cross-sections of data arrays, with axis names and units defined once in the class instance definition;
* The class deals with Fourier transforms, using `numpy.fft` or `pyfftw` under the hood, taking care of fftshifting and making spectral plotting simple;
* Fields can be generated on the space by writing functions of the axis coordinates, and it is easy to perform common Fourier-based operations on them, including convolution, differentiation, or integration.

Use of latticetools starts by instancizing the class `Space`, by providing a tuple of slices which represent the sample spacing (in the same way that a `numpy.ogrid[slices_tuple]` is set up — in fact, this happens under the hood). Once this is done, fields can be generated, which create ndarrays to represent the field. Alternatively, the `Space` instance can be used with external data in all the same ways.


```python
sp = latticetools.Space(
    (slice(-2,2,.01),),
)
field_func = lambda X: np.sin(2 * np.pi * X / .2) * (abs(X) < 1.5)
field = sp.generate_field(field_func)
sp.show(field, '$\sin(X)$', titleas='ylabel')
```


![jpeg](latticetools-intro/output_12_0.jpg)





    [<matplotlib.lines.Line2D at 0x126251c40>]



Taking the discrete Fourier transform can be a hassle, especially when getting one's head around frequency sampling for the n<sup>th</sup> time! latticetools helps by making it easy to produce the DFT, and has special plotting arguments to help show the usually complex fields:


```python
f_dft = sp.dft(field)
sp.show(
    f_dft, 
    dft = True, 
    title = 'Amplitude spectrum of the field', 
    titleas = 'title', 
    vmin = 1e-5,
)
sp.show(
    f_dft, 
    dft = True, 
    title = 'Amplitude spectrum of the field', 
    titleas = 'title', 
    vmin = 1e-3,
    lims = ((-10,10)),
)
```


![jpeg](latticetools-intro/output_14_0.jpg)



![jpeg](latticetools-intro/output_14_1.jpg)





    [<matplotlib.lines.Line2D at 0x117840100>]



In this case as expected, the sinusoidal field with a frequency of 0.2<sup>-1</sup>, its spectral peaks are found at ±5 cycles per unit distance.

latticetools simply uses `numpy.fft` or `pyfftw` to perform frequency operations, and follows the convention of the DC term at the centre of the spectrum.

The DFT can also be taken with zero-padding to enhance spectral sampling, as shown below. This can be accomplished by default, by setting the `factors` argument in the initialization of `Space`.


```python
sp.factors = 5
f_dft = sp.dft(field, axes = 0)
im = sp.show(
    f_dft, 
    dft = True, 
    title = 'Amplitude spectrum of the field', 
    titleas = 'title', 
    vmin = 1e-3,
    lims = ((-10,10)),
)
```


![jpeg](latticetools-intro/output_18_0.jpg)


It might be expected that after oversampling the spectrum, performing the inverse DFT might produce the wrong-sized distribution. However, this is properly handled by telling latticetools what padding factor was used:


```python
f_idft = sp.idft(f_dft, axes = 0)
im = sp.show(
    f_idft, 
    title = 'Inverse DFT of the over-sampled DFT', 
    titleas = 'title',
)
```


![jpeg](latticetools-intro/output_20_0.jpg)


Another operation commonly performed with modelling is a spatial mapping, such as a stretch in the $X$-axis. Such one-to-one spatial mappings are assisted by the `space_warp` function. For example, if a field were defined on a line with coordinate $x$, then the field could be mapped to values at coordinates of $\theta$, where $x=\tan(\theta)$. This is performed under the hood by using scikit-image's warp, but uses coordinates instead of sample indices. First, a new space is defined; then a function is defined which gives the spatial mapping. A warper function can then be made, which when applied to a field gives a new field in the new space:


```python
sp2 = latticetools.Space(
    (slice(-.5, .5, 1 / 1e5),),
    ('$\\theta$',),
    ('$\pi$',)
)
func_dest2source = lambda theta: ((np.tan(theta * np.pi)),)
warper = latticetools.space_warp(sp, sp2, func_dest2source)
field_warped = warper(field)
sp2.show(field_warped, '$\sin(X)$', show = False, titleas='ylabel')
plt.title('Warp according to $X = \\tan(\\theta)$')
plt.show()
```


![jpeg](latticetools-intro/output_22_0.jpg)


For higher-dimensional sample spaces, latticetools can help to visualize cross-sections of it, and keep track of sampling.


```python
spatial_slices = (
    slice(0, 1000, 10),
    slice(0, 500, 10),
    slice(0,8, 1)
)
sp3 = latticetools.Space(
    slices = spatial_slices,
)
```

For closer hacking, the `numpy.ogrid` samples are easily accessible:


```python
describer = lambda array: 'shape: {}, min: {}, max: {}, step: {}'.format(
    array.shape,
    array.min(),
    array.max(),
    array.flatten()[:2].ptp()
)
print('sp3.R is a length {} {} consisting of\n'.format(len(sp3.R), type(sp3.R)),'\n '.join(map(describer,sp3.R)))
```

    sp3.R is a length 3 <class 'list'> consisting of
     shape: (100, 1, 1), min: 0.0, max: 990.0, step: 10.0
     shape: (1, 50, 1), min: 0.0, max: 490.0, step: 10.0
     shape: (1, 1, 8), min: 0.0, max: 7.0, step: 1.0



```python
field = sp3.generate_field(
    func = lambda X,Y,Z: (abs(X - 400) < 300) * np.hypot((Y - (400 - 200 * (Z - 4))) / 300, (X - 400) / 300),
)
```


```python
sp3.show(field, '$F(X,Y)$ @ $Z=4$', axes = (0, 1), coordinates = 4)
sp3.show(field, '$F(Y,Z)$ @ $X=400$', axes = (1, 2), coordinates = 400, aspect = 'auto')
sp3.show(field, '$F(X)$ @ $(Y,Z) = (100,6)$', axes = 0, coordinates = (100, 6))
```


![jpeg](latticetools-intro/output_28_0.jpg)



![jpeg](latticetools-intro/output_28_1.jpg)



![jpeg](latticetools-intro/output_28_2.jpg)





    [<matplotlib.lines.Line2D at 0x117967280>]



In higher-dimensional spaces, performing DFTs in specific dimensions is handled. When using numpy, multidimensional DFTs is usually done with nested function calls within function calls, which gets messy. Here, it is performed by listing the desired axes in one call. The unitary DFT is employed in this implementation, which eases scaling considerations in complex modelling. In this example, the DFT is performed in $Y$ and $Z$, before the resultant field is shown as a 2D distribution along various cross-sections:


```python
field_yz_dft = sp3.dft(field, axes = (1,2))
sp3.show(
    field_yz_dft, 
    '$\mathcal{F}_{(Y,Z)}[F](X,\\nu_Y)$  @ $\\nu_Z=0$ (DC)', 
    axes = (0, 1), 
    dft_axes = (1, 2), 
    coordinates = 0,
)
sp3.show(
    field_yz_dft, 
    '$\mathcal{F}_{(Y,Z)}[F](\\nu_Y,\\nu_Z)$  @ $X=400$', 
    axes = (1, 2), 
    dft_axes = (1, 2), 
    coordinates = 400,
    aspect = 'auto',
)
sp3.show(
    field_yz_dft, 
    '$\mathcal{F}_{(Y,Z)}[F](X)$  @ $(\\nu_Y,\\nu_Z) = (0.25, 0.1)$ unit$^{-1}$', 
    axes = 0, 
    coordinates = (0.25, 0.1),
)
```

    Substituting symbol F from STIXNonUnicode
    Substituting symbol F from STIXNonUnicode



![jpeg](latticetools-intro/output_30_1.jpg)


    Substituting symbol F from STIXNonUnicode
    Substituting symbol F from STIXNonUnicode



![jpeg](latticetools-intro/output_30_3.jpg)


    Substituting symbol F from STIXNonUnicode
    Substituting symbol F from STIXNonUnicode



![jpeg](latticetools-intro/output_30_5.jpg)





    [<matplotlib.lines.Line2D at 0x126fa9940>]



Where latticetools becomes very useful is when using externally-provided distributions. This could be experimental data or images:


```python
from scipy.misc import face
field = face(gray=True)[::-1].astype(int)
```


```python
spatial_slices = tuple(slice(shi) for shi in field.shape)
sp4 = latticetools.Space(
    slices = spatial_slices,
    factors = (3,3),
    axis_units = ['pixel'] * 2,
    vert_axes=0,
)
im = sp4.show(field, 'Scipy\'s face')
im = sp4.show(
    field, 
    'Scipy\'s face; using the matrix-style\nof \"zeroth element in upper left\"',
    origin = 'upper',
)
```


![jpeg](latticetools-intro/output_33_0.jpg)



![jpeg](latticetools-intro/output_33_1.jpg)


A DFT can be taken in any particular axis:


```python
field_xdft = sp4.dft(field, axes = 0)
im = sp4.show(field_xdft, 'X-DFT of Scipy\'s face', dft_axes = 0, vmin = 1e-4)
```


![jpeg](latticetools-intro/output_35_0.jpg)


Plotting into more complex subplots can be performed by setting up the figure using `pyplot`, and then setting the current axis as one of the created axes (`pyplot.sca(...)`). Then, when using `space.show`, use the kwarg `show = False` in order to avoid calling `pyplot.show()`:


```python
dfield_dy = sp4.differentiate(field, axis = 1)
f,a = plt.subplots(1, 3, figsize = (12,3),)
plt.sca(a[0])
sp4.show(
    dfield_dy, 
    '$\partial\mathrm{Face}/\partial Y$', 
    show = False
)
dfdy_xdft = sp4.dft(dfield_dy, axes = 0)
plt.sca(a[1])
sp4.show(
    abs(dfield_dy), 
    '$\left |\partial\mathrm{Face}/\partial Y\\right |$ @ X=400', 
    axes = 1, 
    coordinates = 400,
    show = False
)
plt.sca(a[2])
sp4.show(
    dfdy_xdft, 
    '$\mathcal{F}_X[\partial\mathrm{Face}/\partial Y]$',
    dft_axes = 0,
)
```

    Substituting symbol F from STIXNonUnicode
    Substituting symbol F from STIXNonUnicode



![jpeg](latticetools-intro/output_37_1.jpg)





    (<matplotlib.image.AxesImage at 0x12878f670>,
     <matplotlib.colorbar.Colorbar at 0x1287409a0>)



On the subject of DFTs, latticetools provides a simple way to implement convolutions. This is where padding the input fields comes in handy, in order to avoid periodicity artefacts. Here, a Gaussian blur is demonstrated:


```python
sigma = 5
gauss_func = lambda R: np.exp( - .5 * sum( (Ri / sigma) ** 2 for Ri in R)) / (2 * np.pi * sigma * sigma)
kernel = sp4.generate_field(gauss_func, split = False, origin = True)
sp4.show(kernel, 'Convolution kernel', lims = [[Ri.mean() + i * sigma * 5 for i in (-1,1)] for Ri in sp4.R])
```


![jpeg](latticetools-intro/output_39_0.jpg)





    (<matplotlib.image.AxesImage at 0x11789e190>,
     <matplotlib.colorbar.Colorbar at 0x1178b7b20>)



Convolution involves multiplication in frequency space. When `space.convolve` is called, the input field is padded not with zeros, but with tiles of the input field reversed spatially. This avoids edge artefacts to some extent.


```python
field_convolved = sp4.convolve(field, kernel)
sp4.show(field_convolved, 'Blurred face')
```


![jpeg](latticetools-intro/output_41_0.jpg)





    (<matplotlib.image.AxesImage at 0x126f346a0>,
     <matplotlib.colorbar.Colorbar at 0x126966f40>)




```python
sp4.show(
    sp4.convolve(
        sp4.differentiate(field, axis = 0),
        kernel,
    ), 
    '$\partial\mathrm{Face}/\partial X$, blurred',
)
```


![jpeg](latticetools-intro/output_42_0.jpg)





    (<matplotlib.image.AxesImage at 0x116ec90a0>,
     <matplotlib.colorbar.Colorbar at 0x1272e30d0>)



`space_warp` works in an arbitrary number of dimensions, as demonstrated here:


```python
centre = 340, 650
zoomturn = lambda x, y: (centre[0] + (y - centre[1])**3 / 1e5, centre[1] + (x - centre[0]) / 2.5, )
warper = latticetools.space_warp(sp4, sp4, func_dest2source = zoomturn)

sp4.show(field, 'Face')
sp4.show(warper(field), 'Warped face')
```


![jpeg](latticetools-intro/output_44_0.jpg)



![jpeg](latticetools-intro/output_44_1.jpg)





    (<matplotlib.image.AxesImage at 0x12778b6a0>,
     <matplotlib.colorbar.Colorbar at 0x1277ef070>)


