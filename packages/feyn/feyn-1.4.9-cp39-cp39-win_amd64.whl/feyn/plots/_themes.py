class AbzuColors:
    _abzu_colors = {'hot_magenta': '#FF1EC8',
                    'majorelle_blue': '#4646E6',
                    'spiro_disco_ball': '#0AB4FA',
                    'robin_egg_blue': '#00C8C8',
                    'guppie_green': '#00F082',
                    'golden_yellow': '#FFE10A',
                    'safety_orange': '#FF640A',
                    'dark_jungle_green': '#1E1E1E',
                    'black': '#1E1E1E',
                    'snow': '#FAFAFA',
                    'white': '#FAFAFA'}

    @staticmethod
    def get(color):
        return AbzuColors._abzu_colors.get(color, color)


class FeynTheme:
    # Second color item are the dark mode colors
    highlight = ('guppie_green', 'spiro_disco_ball')
    accent = ('hot_magenta', 'safety_orange')

    light = ('snow', 'dark_jungle_green')
    dark = ('dark_jungle_green', 'snow')

    neutral = ('robin_egg_blue')

    primary = ('majorelle_blue', 'golden_yellow')
    secondary = ('golden_yellow', 'majorelle_blue')

    background = ('#FFFFFF', '#111111')  # Based on jupyterlab settings

    cycle = ['majorelle_blue', 'hot_magenta', 'safety_orange', 'robin_egg_blue', 'guppie_green', 'spiro_disco_ball', 'golden_yellow']
    # Primary, accent, accent_alt, neutral, highlight, hightlight_alt, secondary

    font_sizes = {'small': 10,
                  'medium': 12,
                  'large': 14}

    def __init__(self, dark_mode=False):
        from cycler import cycler
        self.dark_mode = dark_mode
        self.cmaps = {
            'feyn': self._colors(['dark', 'primary', 'accent', 'highlight', 'secondary']),
            'feyn-diverging': self._colors([c[1] for c in self.get_gradient()]),
            'feyn-partial': self._colors(['light', 'primary', 'accent']),
            'feyn-primary': self._colors(['light', 'primary']),
            'feyn-highlight': self._colors(['light', 'highlight']),
            'feyn-secondary': self._colors(['light', 'secondary']),
            'feyn-accent': self._colors(['light', 'accent'])
        }
        self.rcParams = {
            'font.family': 'monospace',
            'lines.linewidth': 3,
            'lines.markersize': 4,
            'lines.color': self.color('dark'),
            'patch.edgecolor': self.color('dark'),
            'text.color': self.color('dark'),
            'figure.facecolor': self.color('background'),
            'figure.edgecolor': self.color('light'),
            'hatch.color': self.color('dark'),
            'boxplot.flierprops.color': self.color('dark'),
            'boxplot.flierprops.markeredgecolor': self.color('dark'),
            'boxplot.boxprops.color': self.color('dark'),
            'boxplot.whiskerprops.color': self.color('dark'),
            'boxplot.capprops.color': self.color('dark'),
            'axes.linewidth': 1.0,
            'axes.titlesize': self.font_sizes['large'],
            'axes.labelsize': self.font_sizes['small'],
            'axes.facecolor': self.color('light'),
            'axes.edgecolor': self.color('dark'),
            'axes.labelcolor': self.color('dark'),
            'axes.prop_cycle': cycler(color=self._colors(self.cycle)),
            'xtick.major.size': 5.5,
            'xtick.minor.size': 3.5,
            'ytick.major.size': 5.5,
            'ytick.minor.size': 3.5,
            'xtick.color': self.color('dark'),
            'ytick.color': self.color('dark'),
            'grid.color': self.color('dark'),
            'legend.fontsize': self.font_sizes['small'],
            'image.cmap': 'feyn',
            'savefig.facecolor': self.color('background'),
            'savefig.edgecolor': self.color('light')
        }

    def color(self, color):
        color = getattr(self, color, color)

        if type(color) == tuple:
            # dark mode support if you follow this pattern as second tuple string
            if self.dark_mode and len(color) == 2:
                color = color[1]
            else:
                color = color[0]

        # Just so we can support abzu color names
        return AbzuColors.get(color)

    def register_cmaps(self):
        _register_linear_cmaps(self.cmaps)
        self.register_rc_params()

    def register_rc_params(self):
        import matplotlib as mpl
        for k, v in self.rcParams.items():
            mpl.rcParams[k] = v

    def _colors(self, colorlist):
        return [self.color(c) for c in colorlist]

    def get_gradient(self):
        return [('low', self.color('accent')),
                ('mid', self.color('light')),
                ('high', self.color('highlight'))] # Should this be primary for the diverging gradient?

    def font_size(self, size):
        # Just trust the user knows to feed the right thing in if not key
        return self.font_sizes.get(size, size)


class MonoTheme(FeynTheme):
    # Linear space of 12 colors between 0xFA and 0x1E (Don't use the darkest ones to improve contrast)
    # R = np.linspace(0xFA,0x1E, 12)
    # print(list(map(lambda r: f"#{int(r):2X}{int(r):2X}{int(r):2X}", R)))
    _grayscale = ['#FAFAFA', '#E6E6E6', '#D2D2D2', '#BEBEBE', '#AAAAAA', '#969696',
                  '#828282', '#6E6E6E', '#5A5A5A', '#464646', '#323232', '#1E1E1E']
    highlight = (_grayscale[3], _grayscale[5])
    accent = (_grayscale[5], _grayscale[3])

    light = (_grayscale[0],  _grayscale[-1])
    dark = (_grayscale[-1], _grayscale[0])

    neutral = (_grayscale[4], _grayscale[-5])

    secondary = (_grayscale[1], _grayscale[-3])
    primary = (_grayscale[-3], _grayscale[1])

    cycle = [_grayscale[-3], _grayscale[5], _grayscale[3],  _grayscale[-5], _grayscale[1]]

    def get_gradient(self):
        # Override gradient
        return [('low', self.color('light')),
                ('mid', self.color('highlight')),
                ('high', self.color('accent'))]


class Theme:
    _themes = {
        'default': FeynTheme(),
        'light': FeynTheme(),
        'dark': FeynTheme(dark_mode=True),
        'mono': MonoTheme(),
        'mono_dark': MonoTheme(dark_mode=True)
    }
    _theme = 'default'

    @staticmethod
    def _get_current():
        """ Get the currently active theme

        Returns:
            FeynTheme -- A FeynTheme instance
        """
        return Theme._themes.get(Theme._theme, 'default')

    @staticmethod
    def color(color):
        """ Helper to get a color from the current theme

        Arguments:
            color {str} -- A color from the theme, either among:
            ['highlight', 'primary', 'secondary', 'accent', 'light', 'dark', 'neutral']
            a color among AbzuColors,
            Colors defined in the theme,
            Hex code (will pass through if not defined)

        Returns:
            [str] -- a string with a color hex code, i.e. '#FF1EC8'
        """
        return Theme._get_current().color(color)

    @staticmethod
    def gradient():
        """ Helper to get a three-step gradient from the current theme

        Returns:
            [Array(tuple(str, str))] -- An array of tuples [('low', <color>), ('mid', <color>), ('high', <color>)]
        """
        return Theme._get_current().get_gradient()

    @staticmethod
    def font_size(size):
        """ Helper to get a font size in pixels from a t-shirt size definition such as:
            ['small', 'medium', 'large']


        Arguments:
            size {str} -- A size in t-shirt sizing

        Returns:
            int -- font size in pixels corresponding to the provided t-shirt size
        """
        return Theme._get_current().font_size(size)

    @staticmethod
    def set_theme(theme='default'):
        """ Sets the theme for visual output in Feyn.

        Arguments:
            theme {str} -- Choose amongst: ['default', 'light', 'dark', 'mono', 'mono_dark']
        """
        # TODO: Should the matplotlib stylings also somehow be affected by theme selection?
        if theme not in Theme._themes:
            raise ValueError(f'Must select among available themes: {list(Theme._themes.keys())}')
        Theme._theme = theme
        Theme._get_current().register_cmaps()


def _register_linear_cmaps(cmaps):
    """Takes a dictionary of cmap names and an array of hex colorstrings in that cmap

    Arguments:
        cmaps {str} -- List[str]
    """
    import matplotlib.cm as cm
    for k, v in cmaps.items():
        cm.register_cmap(name=k, cmap=_get_linear_cmap(k, v))


def _hex_color_to_mpl(colors):
    from matplotlib.colors import hex2color
    return [hex2color(c) for c in colors]


def _get_linear_cmap(name, colors, N=265):
    from matplotlib.colors import LinearSegmentedColormap
    colors = _hex_color_to_mpl(colors)
    return LinearSegmentedColormap.from_list(name, colors, N)
