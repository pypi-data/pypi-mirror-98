import mxdevtool as mx
import mxdevtool.utils as utils



class FlatForward(mx.core_FlatForward):
    def __init__(self, refDate, forward, 
                   dayCounter=mx.Actual365Fixed(), 
                   compounding=mx.Compounded,
                   frequency=mx.Annual):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        self._refDate = refDate
        self._forward = forward
        self._dayCounter = dayCounter
        self._frequency = frequency

        mx.core_FlatForward.__init__(self, _refDate, forward, dayCounter, compounding, frequency)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, FlatForward.__name__)

        refDate = mx.Date(d['refDate'])
        forward = d['forward']
        dayCounter = mx.dayCounterParse(d['dayCounter'])
        frequency = mx.frequencyParse(d['frequency'])

        return FlatForward(refDate, forward, dayCounter, frequency)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['forward'] = self._forward
        res['dayCounter'] = str(self._dayCounter)
        res['frequency'] = mx.frequencyToString(self._frequency)

        return res

    def graph_view(self, typ=None, **kwargs):
        from mxdevtool.view import graph

        # period ( 1Y to 20Y )
        x =  [ v+1 for v in range(20) ]
        y1 = [ self.zeroRate(t, self._compounding).rate() for t in x]

        ydata_d = {'zeroRates': y1}
        graph(name='FlatForward', xdata=x, ydata_d=ydata_d, **kwargs)


class ZeroYieldCurve(mx.core_ZeroYieldCurveExt):
    def __init__(self, refDate, periods, zeroRates, 
                   interpolationType=mx.Interpolator1D.Linear, 
                   extrapolationType=mx.Extrapolator1D.FlatForward, 
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing,
                   compounding=mx.Compounded):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        self._refDate = refDate
        self._periods = utils.toStrList(periods)
        self._zeroRates = zeroRates
        self._interpolationType = interpolationType
        self._extrapolationType = extrapolationType
        self._calendar = _calendar # prevent None 
        self._dayCounter = dayCounter
        self._businessDayConvention = businessDayConvention
        self._compounding = compounding

        mx.core_ZeroYieldCurveExt.__init__(self, _refDate, self._periods, zeroRates, interpolationType, extrapolationType,
                                    _calendar, dayCounter, businessDayConvention, compounding)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroYieldCurve.__name__)

        refDate = str(d['refDate'])
        periods = d['periods']
        zeroRates = d['zeroRates']
        interpolationType = mx.interpolator1DParse(d['interpolationType'])
        extrapolationType = mx.extrapolator1DParse(d['extrapolationType'])

        if extrapolationType == mx.Extrapolator1D.SmithWilson:
            alpha = d['smithwilsonAlpha']
            ufr = d['smithwilsonUFR']
            extrapolation = mx.SmithWilsonExtrapolation(alpha, ufr)
        elif extrapolationType == mx.Extrapolator1D.FlatSpot:
            extrapolation = mx.FlatExtrapolation('spot')
        else:
            extrapolation = mx.FlatExtrapolation('forward')

        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])
        businessDayConvention = mx.businessDayConventionParse(d['businessDayConvention'])
        compounding = mx.compoundingParse(d['compounding'])

        return ZeroYieldCurve(refDate, periods, zeroRates, 
                   interpolationType, 
                   extrapolationType, 
                   calendar,
                   dayCounter, 
                   businessDayConvention,
                   compounding)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['periods'] = self._periods
        res['zeroRates'] = self._zeroRates
        res['interpolationType'] = mx.interpolator1DToString(self._interpolationType)
        res['extrapolationType'] = mx.extrapolator1DToString(self._extrapolationType)
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = mx.businessDayConventionToString(self._businessDayConvention)
        res['compounding'] = mx.compoundingToString(self._compounding)

        return res

    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = [ p.yearFraction() for p in utils.toPeriodClsList(self._periods)]
        y1 = self._zeroRates

        ydata_d = {'zeroRates': y1}
        return graph(name='ZeroYieldCurve', xdata=x, ydata_d=ydata_d, **kwargs)


# familyname : irskrw_krccp only now
class BootstapSwapCurveCCP(mx.core_BootstapSwapCurveCCP):
    def __init__(self, refDate, periods, rateTypes, quotes, 
                interpolationType=mx.Interpolator1D.Linear, 
                extrapolationType=mx.Extrapolator1D.FlatForward, 
                familyname='irskrw_krccp',
                forSettlement=True):

        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        if extrapolationType == mx.Extrapolator1D.SmithWilson:
            extrapolation = mx.SmithWilsonExtrapolation(0.1, 0.042)
        elif extrapolationType == mx.Extrapolator1D.FlatSpot:
            extrapolation = mx.FlatExtrapolation('spot')
        else:
            extrapolation = mx.FlatExtrapolation('forward')

        self._refDate = refDate
        self._periods = utils.toStrList(periods)
        self._rateTypes = rateTypes
        self._quotes = quotes
        self._interpolationType = interpolationType
        self._extrapolationType = extrapolationType
        self._familyname = familyname
        self._forSettlement = forSettlement

        mx.core_BootstapSwapCurveCCP.__init__(self, _refDate, self._periods, rateTypes, quotes, 
                                            interpolationType, extrapolation,
                                            familyname, forSettlement)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BootstapSwapCurveCCP.__name__)

        refDate = d['refDate']
        periods = d['periods']
        rateTypes = d['rateTypes']
        quotes = d['quotes']
        interpolationType = mx.interpolator1DParse(d['interpolationType'])
        extrapolationType = mx.extrapolator1DParse(d['extrapolationType'])

        if extrapolationType == mx.Extrapolator1D.SmithWilson:
            alpha = d['smithwilsonAlpha']
            ufr = d['smithwilsonUFR']
            extrapolation = mx.SmithWilsonExtrapolation(alpha, ufr)
        elif extrapolationType == mx.Extrapolator1D.FlatSpot:
            extrapolation = mx.FlatExtrapolation('spot')
        else:
            extrapolation = mx.FlatExtrapolation('forward')

        familyname = d['familyname']
        forSettlement = d['forSettlement']

        return BootstapSwapCurveCCP(refDate, periods, rateTypes, quotes, 
                                            interpolationType, extrapolation,
                                            familyname, forSettlement)

    def toDict(self):
        res = dict()
        
        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['refDate'] = str(self._refDate)
        res['periods'] = self._periods
        res['rateTypes'] = self._rateTypes
        res['quotes'] = self._quotes
        res['interpolationType'] = mx.interpolator1DToString(self._interpolationType)
        res['extrapolationType'] = mx.extrapolator1DToString(self._extrapolationType)

        if self.extrapolationType == mx.Extrapolator1D.SmithWilson:
            res['smithwilsonAlpha'] = self.smithwilsonAlpha()
            res['smithwilsonUFR'] = self.smithwilsonUFR()

        res['familyname'] = self._familyname
        res['forSettlement'] = self._forSettlement

        return res

    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = [ p.yearFraction() for p in utils.toPeriodClsList(self._quotes)]
        y1 = self._quotes

        ydata_d = {'quotes': y1}

        graph(name='BootstapSwapCurveCCP', xdata=x, ydata_d=ydata_d, **kwargs)


class ZeroSpreadedCurve(mx.core_ZeroSpreadedTermStructure):
    def __init__(self, baseCurve, spread, compounding=mx.Continuous, frequency=mx.Annual):
        
        self._baseCurve = baseCurve
        self._spread = spread
        self._compounding = compounding
        self._frequency = frequency

        mx.core_ZeroSpreadedTermStructure.__init__(self, baseCurve, spread, compounding, frequency)


    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroSpreadedCurve.__name__)

        baseCurve = mrk.get_yieldCurve_d(d['baseCurve'])
        spread = d['spread']
        compounding = mx.compoundingParse(d['compounding'])
        frequency = mx.frequencyParse(d['frequency'])

        return ZeroSpreadedCurve(baseCurve, spread, compounding, frequency)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        
        res['baseCurve'] = self._baseCurve.toDict()
        res['spread'] = self._spread
        res['compounding'] = self._compounding
        res['frequency'] = self._frequency

        return res

    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = kwargs.get('x')

        # period ( 1Y to 20Y )
        x = [v+1 for v in range(20)] if x is None else x
        y1 = [self.zeroRate(t, self._compounding).rate() for t in x]
        ydata_d = {'zeroRates': y1}

        graph(name='ZeroSpreadedCurve', xdata=x, ydata_d=ydata_d, **kwargs)


# class ForwardSpreadedCurve(mx.core_ForwardSpreadedTermStructure):
#     def __init__(self, curve, spread):
#         mx.core_ForwardSpreadedTermStructure.__init__(self, curve, spread)

