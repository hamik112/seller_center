Date.CultureInfo = {
    name: "en-US",
    englishName: "English (United States)",
    nativeName: "English (United States)",
    dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    abbreviatedDayNames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    shortestDayNames: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    firstLetterDayNames: ["S", "M", "T", "W", "T", "F", "S"],
    monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    abbreviatedMonthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    amDesignator: "AM",
    pmDesignator: "PM",
    firstDayOfWeek: 0,
    twoDigitYearMax: 2029,
    dateElementOrder: "mdy",
    formatPatterns: {
        shortDate: "M/d/yyyy",
        longDate: "dddd, MMMM dd, yyyy",
        shortTime: "h:mm tt",
        longTime: "h:mm:ss tt",
        fullDateTime: "dddd, MMMM dd, yyyy h:mm:ss tt",
        sortableDateTime: "yyyy-MM-ddTHH:mm:ss",
        universalSortableDateTime: "yyyy-MM-dd HH:mm:ssZ",
        rfc1123: "ddd, dd MMM yyyy HH:mm:ss GMT",
        monthDay: "MMMM dd",
        yearMonth: "MMMM, yyyy"
    },
    regexPatterns: {
        jan: /^jan(uary)?/i,
        feb: /^feb(ruary)?/i,
        mar: /^mar(ch)?/i,
        apr: /^apr(il)?/i,
        may: /^may/i,
        jun: /^jun(e)?/i,
        jul: /^jul(y)?/i,
        aug: /^aug(ust)?/i,
        sep: /^sep(t(ember)?)?/i,
        oct: /^oct(ober)?/i,
        nov: /^nov(ember)?/i,
        dec: /^dec(ember)?/i,
        sun: /^su(n(day)?)?/i,
        mon: /^mo(n(day)?)?/i,
        tue: /^tu(e(s(day)?)?)?/i,
        wed: /^we(d(nesday)?)?/i,
        thu: /^th(u(r(s(day)?)?)?)?/i,
        fri: /^fr(i(day)?)?/i,
        sat: /^sa(t(urday)?)?/i,
        future: /^next/i,
        past: /^last|past|prev(ious)?/i,
        add: /^(\+|after|from)/i,
        subtract: /^(\-|before|ago)/i,
        yesterday: /^yesterday/i,
        today: /^t(oday)?/i,
        tomorrow: /^tomorrow/i,
        now: /^n(ow)?/i,
        millisecond: /^ms|milli(second)?s?/i,
        second: /^sec(ond)?s?/i,
        minute: /^min(ute)?s?/i,
        hour: /^h(ou)?rs?/i,
        week: /^w(ee)?k/i,
        month: /^m(o(nth)?s?)?/i,
        day: /^d(ays?)?/i,
        year: /^y((ea)?rs?)?/i,
        shortMeridian: /^(a|p)/i,
        longMeridian: /^(a\.?m?\.?|p\.?m?\.?)/i,
        timezone: /^((e(s|d)t|c(s|d)t|m(s|d)t|p(s|d)t)|((gmt)?\s*(\+|\-)\s*\d\d\d\d?)|gmt)/i,
        ordinalSuffix: /^\s*(st|nd|rd|th)/i,
        timeContext: /^\s*(\:|a|p)/i
    },
    abbreviatedTimeZoneStandard: {
        GMT: "-000",
        EST: "-0400",
        CST: "-0500",
        MST: "-0600",
        PST: "-0700"
    },
    abbreviatedTimeZoneDST: {
        GMT: "-000",
        EDT: "-0500",
        CDT: "-0600",
        MDT: "-0700",
        PDT: "-0800"
    }
};
Date.getMonthNumberFromName = function(name) {
    var n = Date.CultureInfo.monthNames,
    m = Date.CultureInfo.abbreviatedMonthNames,
    s = name.toLowerCase();
    for (var i = 0; i < n.length; i++) {
        if (n[i].toLowerCase() == s || m[i].toLowerCase() == s) {
            return i;
        }
    }
    return - 1;
};
Date.getDayNumberFromName = function(name) {
    var n = Date.CultureInfo.dayNames,
    m = Date.CultureInfo.abbreviatedDayNames,
    o = Date.CultureInfo.shortestDayNames,
    s = name.toLowerCase();
    for (var i = 0; i < n.length; i++) {
        if (n[i].toLowerCase() == s || m[i].toLowerCase() == s) {
            return i;
        }
    }
    return - 1;
};
Date.isLeapYear = function(year) {
    return (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0));
};
Date.getDaysInMonth = function(year, month) {
    return [31, (Date.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
};
Date.getTimezoneOffset = function(s, dst) {
    return (dst || false) ? Date.CultureInfo.abbreviatedTimeZoneDST[s.toUpperCase()] : Date.CultureInfo.abbreviatedTimeZoneStandard[s.toUpperCase()];
};
Date.getTimezoneAbbreviation = function(offset, dst) {
    var n = (dst || false) ? Date.CultureInfo.abbreviatedTimeZoneDST: Date.CultureInfo.abbreviatedTimeZoneStandard,
    p;
    for (p in n) {
        if (n[p] === offset) {
            return p;
        }
    }
    return null;
};
Date.prototype.clone = function() {
    return new Date(this.getTime());
};
Date.prototype.compareTo = function(date) {
    if (isNaN(this)) {
        throw new Error(this);
    }
    if (date instanceof Date && !isNaN(date)) {
        return (this > date) ? 1 : (this < date) ? -1 : 0;
    } else {
        throw new TypeError(date);
    }
};
Date.prototype.equals = function(date) {
    return (this.compareTo(date) === 0);
};
Date.prototype.between = function(start, end) {
    var t = this.getTime();
    return t >= start.getTime() && t <= end.getTime();
};
Date.prototype.addMilliseconds = function(value) {
    this.setMilliseconds(this.getMilliseconds() + value);
    return this;
};
Date.prototype.addSeconds = function(value) {
    return this.addMilliseconds(value * 1000);
};
Date.prototype.addMinutes = function(value) {
    return this.addMilliseconds(value * 60000);
};
Date.prototype.addHours = function(value) {
    return this.addMilliseconds(value * 3600000);
};
Date.prototype.addDays = function(value) {
    return this.addMilliseconds(value * 86400000);
};
Date.prototype.addWeeks = function(value) {
    return this.addMilliseconds(value * 604800000);
};
Date.prototype.addMonths = function(value) {
    var n = this.getDate();
    this.setDate(1);
    this.setMonth(this.getMonth() + value);
    this.setDate(Math.min(n, this.getDaysInMonth()));
    return this;
};
Date.prototype.addYears = function(value) {
    return this.addMonths(value * 12);
};
Date.prototype.add = function(config) {
    if (typeof config == "number") {
        this._orient = config;
        return this;
    }
    var x = config;
    if (x.millisecond || x.milliseconds) {
        this.addMilliseconds(x.millisecond || x.milliseconds);
    }
    if (x.second || x.seconds) {
        this.addSeconds(x.second || x.seconds);
    }
    if (x.minute || x.minutes) {
        this.addMinutes(x.minute || x.minutes);
    }
    if (x.hour || x.hours) {
        this.addHours(x.hour || x.hours);
    }
    if (x.month || x.months) {
        this.addMonths(x.month || x.months);
    }
    if (x.year || x.years) {
        this.addYears(x.year || x.years);
    }
    if (x.day || x.days) {
        this.addDays(x.day || x.days);
    }
    return this;
};
Date._validate = function(value, min, max, name) {
    if (typeof value != "number") {
        throw new TypeError(value + " is not a Number.");
    } else {
        if (value < min || value > max) {
            throw new RangeError(value + " is not a valid value for " + name + ".");
        }
    }
    return true;
};
Date.validateMillisecond = function(n) {
    return Date._validate(n, 0, 999, "milliseconds");
};
Date.validateSecond = function(n) {
    return Date._validate(n, 0, 59, "seconds");
};
Date.validateMinute = function(n) {
    return Date._validate(n, 0, 59, "minutes");
};
Date.validateHour = function(n) {
    return Date._validate(n, 0, 23, "hours");
};
Date.validateDay = function(n, year, month) {
    return Date._validate(n, 1, Date.getDaysInMonth(year, month), "days");
};
Date.validateMonth = function(n) {
    return Date._validate(n, 0, 11, "months");
};
Date.validateYear = function(n) {
    return Date._validate(n, 1, 9999, "seconds");
};
Date.prototype.set = function(config) {
    var x = config;
    if (!x.millisecond && x.millisecond !== 0) {
        x.millisecond = -1;
    }
    if (!x.second && x.second !== 0) {
        x.second = -1;
    }
    if (!x.minute && x.minute !== 0) {
        x.minute = -1;
    }
    if (!x.hour && x.hour !== 0) {
        x.hour = -1;
    }
    if (!x.day && x.day !== 0) {
        x.day = -1;
    }
    if (!x.month && x.month !== 0) {
        x.month = -1;
    }
    if (!x.year && x.year !== 0) {
        x.year = -1;
    }
    if (x.millisecond != -1 && Date.validateMillisecond(x.millisecond)) {
        this.addMilliseconds(x.millisecond - this.getMilliseconds());
    }
    if (x.second != -1 && Date.validateSecond(x.second)) {
        this.addSeconds(x.second - this.getSeconds());
    }
    if (x.minute != -1 && Date.validateMinute(x.minute)) {
        this.addMinutes(x.minute - this.getMinutes());
    }
    if (x.hour != -1 && Date.validateHour(x.hour)) {
        this.addHours(x.hour - this.getHours());
    }
    if (x.month !== -1 && Date.validateMonth(x.month)) {
        this.addMonths(x.month - this.getMonth());
    }
    if (x.year != -1 && Date.validateYear(x.year)) {
        this.addYears(x.year - this.getFullYear());
    }
    if (x.day != -1 && Date.validateDay(x.day, this.getFullYear(), this.getMonth())) {
        this.addDays(x.day - this.getDate());
    }
    if (x.timezone) {
        this.setTimezone(x.timezone);
    }
    if (x.timezoneOffset) {
        this.setTimezoneOffset(x.timezoneOffset);
    }
    return this;
};
Date.prototype.clearTime = function() {
    this.setHours(0);
    this.setMinutes(0);
    this.setSeconds(0);
    this.setMilliseconds(0);
    return this;
};
Date.prototype.isLeapYear = function() {
    var y = this.getFullYear();
    return (((y % 4 === 0) && (y % 100 !== 0)) || (y % 400 === 0));
};
Date.prototype.isWeekday = function() {
    return ! (this.is().sat() || this.is().sun());
};
Date.prototype.getDaysInMonth = function() {
    return Date.getDaysInMonth(this.getFullYear(), this.getMonth());
};
Date.prototype.moveToFirstDayOfMonth = function() {
    return this.set({
        day: 1
    });
};
Date.prototype.moveToLastDayOfMonth = function() {
    return this.set({
        day: this.getDaysInMonth()
    });
};
Date.prototype.moveToDayOfWeek = function(day, orient) {
    var diff = (day - this.getDay() + 7 * (orient || +1)) % 7;
    return this.addDays((diff === 0) ? diff += 7 * (orient || +1) : diff);
};
Date.prototype.moveToMonth = function(month, orient) {
    var diff = (month - this.getMonth() + 12 * (orient || +1)) % 12;
    return this.addMonths((diff === 0) ? diff += 12 * (orient || +1) : diff);
};
Date.prototype.getDayOfYear = function() {
    return Math.floor((this - new Date(this.getFullYear(), 0, 1)) / 86400000);
};
Date.prototype.getWeekOfYear = function(firstDayOfWeek) {
    var y = this.getFullYear(),
    m = this.getMonth(),
    d = this.getDate();
    var dow = firstDayOfWeek || Date.CultureInfo.firstDayOfWeek;
    var offset = 7 + 1 - new Date(y, 0, 1).getDay();
    if (offset == 8) {
        offset = 1;
    }
    var daynum = ((Date.UTC(y, m, d, 0, 0, 0) - Date.UTC(y, 0, 1, 0, 0, 0)) / 86400000) + 1;
    var w = Math.floor((daynum - offset + 7) / 7);
    if (w === dow) {
        y--;
        var prevOffset = 7 + 1 - new Date(y, 0, 1).getDay();
        if (prevOffset == 2 || prevOffset == 8) {
            w = 53;
        } else {
            w = 52;
        }
    }
    return w;
};
Date.prototype.isDST = function() {
    return this.toString().match(/(E|C|M|P)(S|D)T/)[2] == "D";
};
Date.prototype.getTimezone = function() {
    return Date.getTimezoneAbbreviation(this.getUTCOffset, this.isDST());
};
Date.prototype.setTimezoneOffset = function(s) {
    var here = this.getTimezoneOffset(),
    there = Number(s) * -6 / 10;
    this.addMinutes(there - here);
    return this;
};
Date.prototype.setTimezone = function(s) {
    return this.setTimezoneOffset(Date.getTimezoneOffset(s));
};
Date.prototype.getUTCOffset = function() {
    var n = this.getTimezoneOffset() * -10 / 6,
    r;
    if (n < 0) {
        r = (n - 10000).toString();
        return r[0] + r.substr(2);
    } else {
        r = (n + 10000).toString();
        return "+" + r.substr(1);
    }
};
Date.prototype.getDayName = function(abbrev) {
    return abbrev ? Date.CultureInfo.abbreviatedDayNames[this.getDay()] : Date.CultureInfo.dayNames[this.getDay()];
};
Date.prototype.getMonthName = function(abbrev) {
    return abbrev ? Date.CultureInfo.abbreviatedMonthNames[this.getMonth()] : Date.CultureInfo.monthNames[this.getMonth()];
};
Date.prototype._toString = Date.prototype.toString;
Date.prototype.toString = function(format) {
    var self = this;
    var p = function p(s) {
        return (s.toString().length == 1) ? "0" + s: s;
    };
    return format ? format.replace(/dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?/g,
    function(format) {
        switch (format) {
        case "hh":
            return p(self.getHours() < 13 ? self.getHours() : (self.getHours() - 12));
        case "h":
            return self.getHours() < 13 ? self.getHours() : (self.getHours() - 12);
        case "HH":
            return p(self.getHours());
        case "H":
            return self.getHours();
        case "mm":
            return p(self.getMinutes());
        case "m":
            return self.getMinutes();
        case "ss":
            return p(self.getSeconds());
        case "s":
            return self.getSeconds();
        case "yyyy":
            return self.getFullYear();
        case "yy":
            return self.getFullYear().toString().substring(2, 4);
        case "dddd":
            return self.getDayName();
        case "ddd":
            return self.getDayName(true);
        case "dd":
            return p(self.getDate());
        case "d":
            return self.getDate().toString();
        case "MMMM":
            return self.getMonthName();
        case "MMM":
            return self.getMonthName(true);
        case "MM":
            return p((self.getMonth() + 1));
        case "M":
            return self.getMonth() + 1;
        case "t":
            return self.getHours() < 12 ? Date.CultureInfo.amDesignator.substring(0, 1) : Date.CultureInfo.pmDesignator.substring(0, 1);
        case "tt":
            return self.getHours() < 12 ? Date.CultureInfo.amDesignator: Date.CultureInfo.pmDesignator;
        case "zzz":
        case "zz":
        case "z":
            return "";
        }
    }):
    this._toString();
};
Date.now = function() {
    return new Date();
};
Date.today = function() {
    return Date.now().clearTime();
};
Date.prototype._orient = +1;
Date.prototype.next = function() {
    this._orient = +1;
    return this;
};
Date.prototype.last = Date.prototype.prev = Date.prototype.previous = function() {
    this._orient = -1;
    return this;
};
Date.prototype._is = false;
Date.prototype.is = function() {
    this._is = true;
    return this;
};
Number.prototype._dateElement = "day";
Number.prototype.fromNow = function() {
    var c = {};
    c[this._dateElement] = this;
    return Date.now().add(c);
};
Number.prototype.ago = function() {
    var c = {};
    c[this._dateElement] = this * -1;
    return Date.now().add(c);
}; (function() {
    var $D = Date.prototype,
    $N = Number.prototype;
    var dx = ("sunday monday tuesday wednesday thursday friday saturday").split(/\s/),
    mx = ("january february march april may june july august september october november december").split(/\s/),
    px = ("Millisecond Second Minute Hour Day Week Month Year").split(/\s/),
    de;
    var df = function(n) {
        return function() {
            if (this._is) {
                this._is = false;
                return this.getDay() == n;
            }
            return this.moveToDayOfWeek(n, this._orient);
        };
    };
    for (var i = 0; i < dx.length; i++) {
        $D[dx[i]] = $D[dx[i].substring(0, 3)] = df(i);
    }
    var mf = function(n) {
        return function() {
            if (this._is) {
                this._is = false;
                return this.getMonth() === n;
            }
            return this.moveToMonth(n, this._orient);
        };
    };
    for (var j = 0; j < mx.length; j++) {
        $D[mx[j]] = $D[mx[j].substring(0, 3)] = mf(j);
    }
    var ef = function(j) {
        return function() {
            if (j.substring(j.length - 1) != "s") {
                j += "s";
            }
            return this["add" + j](this._orient);
        };
    };
    var nf = function(n) {
        return function() {
            this._dateElement = n;
            return this;
        };
    };
    for (var k = 0; k < px.length; k++) {
        de = px[k].toLowerCase();
        $D[de] = $D[de + "s"] = ef(px[k]);
        $N[de] = $N[de + "s"] = nf(de);
    }
} ());
Date.prototype.toJSONString = function() {
    return this.toString("yyyy-MM-ddThh:mm:ssZ");
};
Date.prototype.toShortDateString = function() {
    return this.toString(Date.CultureInfo.formatPatterns.shortDatePattern);
};
Date.prototype.toLongDateString = function() {
    return this.toString(Date.CultureInfo.formatPatterns.longDatePattern);
};
Date.prototype.toShortTimeString = function() {
    return this.toString(Date.CultureInfo.formatPatterns.shortTimePattern);
};
Date.prototype.toLongTimeString = function() {
    return this.toString(Date.CultureInfo.formatPatterns.longTimePattern);
};
Date.prototype.getOrdinal = function() {
    switch (this.getDate()) {
    case 1:
    case 21:
    case 31:
        return "st";
    case 2:
    case 22:
        return "nd";
    case 3:
    case 23:
        return "rd";
    default:
        return "th";
    }
}; (function() {
    Date.Parsing = {
        Exception: function(s) {
            this.message = "Parse error at '" + s.substring(0, 10) + " ...'";
        }
    };
    var $P = Date.Parsing;
    var _ = $P.Operators = {
        rtoken: function(r) {
            return function(s) {
                var mx = s.match(r);
                if (mx) {
                    return ([mx[0], s.substring(mx[0].length)]);
                } else {
                    throw new $P.Exception(s);
                }
            };
        },
        token: function(s) {
            return function(s) {
                return _.rtoken(new RegExp("^s*" + s + "s*"))(s);
            };
        },
        stoken: function(s) {
            return _.rtoken(new RegExp("^" + s));
        },
        until: function(p) {
            return function(s) {
                var qx = [],
                rx = null;
                while (s.length) {
                    try {
                        rx = p.call(this, s);
                    } catch(e) {
                        qx.push(rx[0]);
                        s = rx[1];
                        continue;
                    }
                    break;
                }
                return [qx, s];
            };
        },
        many: function(p) {
            return function(s) {
                var rx = [],
                r = null;
                while (s.length) {
                    try {
                        r = p.call(this, s);
                    } catch(e) {
                        return [rx, s];
                    }
                    rx.push(r[0]);
                    s = r[1];
                }
                return [rx, s];
            };
        },
        optional: function(p) {
            return function(s) {
                var r = null;
                try {
                    r = p.call(this, s);
                } catch(e) {
                    return [null, s];
                }
                return [r[0], r[1]];
            };
        },
        not: function(p) {
            return function(s) {
                try {
                    p.call(this, s);
                } catch(e) {
                    return [null, s];
                }
                throw new $P.Exception(s);
            };
        },
        ignore: function(p) {
            return p ?
            function(s) {
                var r = null;
                r = p.call(this, s);
                return [null, r[1]];
            }: null;
        },
        product: function() {
            var px = arguments[0],
            qx = Array.prototype.slice.call(arguments, 1),
            rx = [];
            for (var i = 0; i < px.length; i++) {
                rx.push(_.each(px[i], qx));
            }
            return rx;
        },
        cache: function(rule) {
            var cache = {},
            r = null;
            return function(s) {
                try {
                    r = cache[s] = (cache[s] || rule.call(this, s));
                } catch(e) {
                    r = cache[s] = e;
                }
                if (r instanceof $P.Exception) {
                    throw r;
                } else {
                    return r;
                }
            };
        },
        any: function() {
            var px = arguments;
            return function(s) {
                var r = null;
                for (var i = 0; i < px.length; i++) {
                    if (px[i] == null) {
                        continue;
                    }
                    try {
                        r = (px[i].call(this, s));
                    } catch(e) {
                        r = null;
                    }
                    if (r) {
                        return r;
                    }
                }
                throw new $P.Exception(s);
            };
        },
        each: function() {
            var px = arguments;
            return function(s) {
                var rx = [],
                r = null;
                for (var i = 0; i < px.length; i++) {
                    if (px[i] == null) {
                        continue;
                    }
                    try {
                        r = (px[i].call(this, s));
                    } catch(e) {
                        throw new $P.Exception(s);
                    }
                    rx.push(r[0]);
                    s = r[1];
                }
                return [rx, s];
            };
        },
        all: function() {
            var px = arguments,
            _ = _;
            return _.each(_.optional(px));
        },
        sequence: function(px, d, c) {
            d = d || _.rtoken(/^\s*/);
            c = c || null;
            if (px.length == 1) {
                return px[0];
            }
            return function(s) {
                var r = null,
                q = null;
                var rx = [];
                for (var i = 0; i < px.length; i++) {
                    try {
                        r = px[i].call(this, s);
                    } catch(e) {
                        break;
                    }
                    rx.push(r[0]);
                    try {
                        q = d.call(this, r[1]);
                    } catch(ex) {
                        q = null;
                        break;
                    }
                    s = q[1];
                }
                if (!r) {
                    throw new $P.Exception(s);
                }
                if (q) {
                    throw new $P.Exception(q[1]);
                }
                if (c) {
                    try {
                        r = c.call(this, r[1]);
                    } catch(ey) {
                        throw new $P.Exception(r[1]);
                    }
                }
                return [rx, (r ? r[1] : s)];
            };
        },
        between: function(d1, p, d2) {
            d2 = d2 || d1;
            var _fn = _.each(_.ignore(d1), p, _.ignore(d2));
            return function(s) {
                var rx = _fn.call(this, s);
                return [[rx[0][0], r[0][2]], rx[1]];
            };
        },
        list: function(p, d, c) {
            d = d || _.rtoken(/^\s*/);
            c = c || null;
            return (p instanceof Array ? _.each(_.product(p.slice(0, -1), _.ignore(d)), p.slice( - 1), _.ignore(c)) : _.each(_.many(_.each(p, _.ignore(d))), px, _.ignore(c)));
        },
        set: function(px, d, c) {
            d = d || _.rtoken(/^\s*/);
            c = c || null;
            return function(s) {
                var r = null,
                p = null,
                q = null,
                rx = null,
                best = [[], s],
                last = false;
                for (var i = 0; i < px.length; i++) {
                    q = null;
                    p = null;
                    r = null;
                    last = (px.length == 1);
                    try {
                        r = px[i].call(this, s);
                    } catch(e) {
                        continue;
                    }
                    rx = [[r[0]], r[1]];
                    if (r[1].length > 0 && !last) {
                        try {
                            q = d.call(this, r[1]);
                        } catch(ex) {
                            last = true;
                        }
                    } else {
                        last = true;
                    }
                    if (!last && q[1].length === 0) {
                        last = true;
                    }
                    if (!last) {
                        var qx = [];
                        for (var j = 0; j < px.length; j++) {
                            if (i != j) {
                                qx.push(px[j]);
                            }
                        }
                        p = _.set(qx, d).call(this, q[1]);
                        if (p[0].length > 0) {
                            rx[0] = rx[0].concat(p[0]);
                            rx[1] = p[1];
                        }
                    }
                    if (rx[1].length < best[1].length) {
                        best = rx;
                    }
                    if (best[1].length === 0) {
                        break;
                    }
                }
                if (best[0].length === 0) {
                    return best;
                }
                if (c) {
                    try {
                        q = c.call(this, best[1]);
                    } catch(ey) {
                        throw new $P.Exception(best[1]);
                    }
                    best[1] = q[1];
                }
                return best;
            };
        },
        forward: function(gr, fname) {
            return function(s) {
                return gr[fname].call(this, s);
            };
        },
        replace: function(rule, repl) {
            return function(s) {
                var r = rule.call(this, s);
                return [repl, r[1]];
            };
        },
        process: function(rule, fn) {
            return function(s) {
                var r = rule.call(this, s);
                return [fn.call(this, r[0]), r[1]];
            };
        },
        min: function(min, rule) {
            return function(s) {
                var rx = rule.call(this, s);
                if (rx[0].length < min) {
                    throw new $P.Exception(s);
                }
                return rx;
            };
        }
    };
    var _generator = function(op) {
        return function() {
            var args = null,
            rx = [];
            if (arguments.length > 1) {
                args = Array.prototype.slice.call(arguments);
            } else {
                if (arguments[0] instanceof Array) {
                    args = arguments[0];
                }
            }
            if (args) {
                for (var i = 0,
                px = args.shift(); i < px.length; i++) {
                    args.unshift(px[i]);
                    rx.push(op.apply(null, args));
                    args.shift();
                    return rx;
                }
            } else {
                return op.apply(null, arguments);
            }
        };
    };
    var gx = "optional not ignore cache".split(/\s/);
    for (var i = 0; i < gx.length; i++) {
        _[gx[i]] = _generator(_[gx[i]]);
    }
    var _vector = function(op) {
        return function() {
            if (arguments[0] instanceof Array) {
                return op.apply(null, arguments[0]);
            } else {
                return op.apply(null, arguments);
            }
        };
    };
    var vx = "each any all".split(/\s/);
    for (var j = 0; j < vx.length; j++) {
        _[vx[j]] = _vector(_[vx[j]]);
    }
} ()); (function() {
    var flattenAndCompact = function(ax) {
        var rx = [];
        for (var i = 0; i < ax.length; i++) {
            if (ax[i] instanceof Array) {
                rx = rx.concat(flattenAndCompact(ax[i]));
            } else {
                if (ax[i]) {
                    rx.push(ax[i]);
                }
            }
        }
        return rx;
    };
    Date.Grammar = {};
    Date.Translator = {
        hour: function(s) {
            return function() {
                this.hour = Number(s);
            };
        },
        minute: function(s) {
            return function() {
                this.minute = Number(s);
            };
        },
        second: function(s) {
            return function() {
                this.second = Number(s);
            };
        },
        meridian: function(s) {
            return function() {
                this.meridian = s.slice(0, 1).toLowerCase();
            };
        },
        timezone: function(s) {
            return function() {
                var n = s.replace(/[^\d\+\-]/g, "");
                if (n.length) {
                    this.timezoneOffset = Number(n);
                } else {
                    this.timezone = s.toLowerCase();
                }
            };
        },
        day: function(x) {
            var s = x[0];
            return function() {
                this.day = Number(s.match(/\d+/)[0]);
            };
        },
        month: function(s) {
            return function() {
                this.month = ((s.length == 3) ? Date.getMonthNumberFromName(s) : (Number(s) - 1));
            };
        },
        year: function(s) {
            return function() {
                var n = Number(s);
                this.year = ((s.length > 2) ? n: (n + (((n + 2000) < Date.CultureInfo.twoDigitYearMax) ? 2000 : 1900)));
            };
        },
        rday: function(s) {
            return function() {
                switch (s) {
                case "yesterday":
                    this.days = -1;
                    break;
                case "tomorrow":
                    this.days = 1;
                    break;
                case "today":
                    this.days = 0;
                    break;
                case "now":
                    this.days = 0;
                    this.now = true;
                    break;
                }
            };
        },
        finishExact: function(x) {
            x = (x instanceof Array) ? x: [x];
            var now = new Date();
            this.year = now.getFullYear();
            this.month = now.getMonth();
            this.day = 1;
            this.hour = 0;
            this.minute = 0;
            this.second = 0;
            for (var i = 0; i < x.length; i++) {
                if (x[i]) {
                    x[i].call(this);
                }
            }
            this.hour = (this.meridian == "p" && this.hour < 13) ? this.hour + 12 : this.hour;
            if (this.day > Date.getDaysInMonth(this.year, this.month)) {
                throw new RangeError(this.day + " is not a valid value for days.");
            }
            var r = new Date(this.year, this.month, this.day, this.hour, this.minute, this.second);
            if (this.timezone) {
                r.set({
                    timezone: this.timezone
                });
            } else {
                if (this.timezoneOffset) {
                    r.set({
                        timezoneOffset: this.timezoneOffset
                    });
                }
            }
            return r;
        },
        finish: function(x) {
            x = (x instanceof Array) ? flattenAndCompact(x) : [x];
            if (x.length === 0) {
                return null;
            }
            for (var i = 0; i < x.length; i++) {
                if (typeof x[i] == "function") {
                    x[i].call(this);
                }
            }
            if (this.now) {
                return new Date();
            }
            var today = Date.today();
            var method = null;
            var expression = !!(this.days != null || this.orient || this.operator);
            if (expression) {
                var gap, mod, orient;
                orient = ((this.orient == "past" || this.operator == "subtract") ? -1 : 1);
                if (this.weekday) {
                    this.unit = "day";
                    gap = (Date.getDayNumberFromName(this.weekday) - today.getDay());
                    mod = 7;
                    this.days = gap ? ((gap + (orient * mod)) % mod) : (orient * mod);
                }
                if (this.month) {
                    this.unit = "month";
                    gap = (this.month - today.getMonth());
                    mod = 12;
                    this.months = gap ? ((gap + (orient * mod)) % mod) : (orient * mod);
                    this.month = null;
                }
                if (!this.unit) {
                    this.unit = "day";
                }
                if (this[this.unit + "s"] == null || this.operator != null) {
                    if (!this.value) {
                        this.value = 1;
                    }
                    if (this.unit == "week") {
                        this.unit = "day";
                        this.value = this.value * 7;
                    }
                    this[this.unit + "s"] = this.value * orient;
                }
                return today.add(this);
            } else {
                if (this.meridian && this.hour) {
                    this.hour = (this.hour < 13 && this.meridian == "p") ? this.hour + 12 : this.hour;
                }
                if (this.weekday && !this.day) {
                    this.day = (today.addDays((Date.getDayNumberFromName(this.weekday) - today.getDay()))).getDate();
                }
                if (this.month && !this.day) {
                    this.day = 1;
                }
                return today.set(this);
            }
        }
    };
    var _ = Date.Parsing.Operators,
    g = Date.Grammar,
    t = Date.Translator,
    _fn;
    g.datePartDelimiter = _.rtoken(/^([\s\-\.\,\/\x27]+)/);
    g.timePartDelimiter = _.stoken(":");
    g.whiteSpace = _.rtoken(/^\s*/);
    g.generalDelimiter = _.rtoken(/^(([\s\,]|at|on)+)/);
    var _C = {};
    g.ctoken = function(keys) {
        var fn = _C[keys];
        if (!fn) {
            var c = Date.CultureInfo.regexPatterns;
            var kx = keys.split(/\s+/),
            px = [];
            for (var i = 0; i < kx.length; i++) {
                px.push(_.replace(_.rtoken(c[kx[i]]), kx[i]));
            }
            fn = _C[keys] = _.any.apply(null, px);
        }
        return fn;
    };
    g.ctoken2 = function(key) {
        return _.rtoken(Date.CultureInfo.regexPatterns[key]);
    };
    g.h = _.cache(_.process(_.rtoken(/^(0[0-9]|1[0-2]|[1-9])/), t.hour));
    g.hh = _.cache(_.process(_.rtoken(/^(0[0-9]|1[0-2])/), t.hour));
    g.H = _.cache(_.process(_.rtoken(/^([0-1][0-9]|2[0-3]|[0-9])/), t.hour));
    g.HH = _.cache(_.process(_.rtoken(/^([0-1][0-9]|2[0-3])/), t.hour));
    g.m = _.cache(_.process(_.rtoken(/^([0-5][0-9]|[0-9])/), t.minute));
    g.mm = _.cache(_.process(_.rtoken(/^[0-5][0-9]/), t.minute));
    g.s = _.cache(_.process(_.rtoken(/^([0-5][0-9]|[0-9])/), t.second));
    g.ss = _.cache(_.process(_.rtoken(/^[0-5][0-9]/), t.second));
    g.hms = _.cache(_.sequence([g.H, g.mm, g.ss], g.timePartDelimiter));
    g.t = _.cache(_.process(g.ctoken2("shortMeridian"), t.meridian));
    g.tt = _.cache(_.process(g.ctoken2("longMeridian"), t.meridian));
    g.z = _.cache(_.process(_.rtoken(/^(\+|\-)?\s*\d\d\d\d?/), t.timezone));
    g.zz = _.cache(_.process(_.rtoken(/^(\+|\-)\s*\d\d\d\d/), t.timezone));
    g.zzz = _.cache(_.process(g.ctoken2("timezone"), t.timezone));
    g.timeSuffix = _.each(_.ignore(g.whiteSpace), _.set([g.tt, g.zzz]));
    g.time = _.each(_.optional(_.ignore(_.stoken("T"))), g.hms, g.timeSuffix);
    g.d = _.cache(_.process(_.each(_.rtoken(/^([0-2]\d|3[0-1]|\d)/), _.optional(g.ctoken2("ordinalSuffix"))), t.day));
    g.dd = _.cache(_.process(_.each(_.rtoken(/^([0-2]\d|3[0-1])/), _.optional(g.ctoken2("ordinalSuffix"))), t.day));
    g.ddd = g.dddd = _.cache(_.process(g.ctoken("sun mon tue wed thu fri sat"),
    function(s) {
        return function() {
            this.weekday = s;
        };
    }));
    g.M = _.cache(_.process(_.rtoken(/^(1[0-2]|0\d|\d)/), t.month));
    g.MM = _.cache(_.process(_.rtoken(/^(1[0-2]|0\d)/), t.month));
    g.MMM = g.MMMM = _.cache(_.process(g.ctoken("jan feb mar apr may jun jul aug sep oct nov dec"), t.month));
    g.y = _.cache(_.process(_.rtoken(/^(\d\d?)/), t.year));
    g.yy = _.cache(_.process(_.rtoken(/^(\d\d)/), t.year));
    g.yyy = _.cache(_.process(_.rtoken(/^(\d\d?\d?\d?)/), t.year));
    g.yyyy = _.cache(_.process(_.rtoken(/^(\d\d\d\d)/), t.year));
    _fn = function() {
        return _.each(_.any.apply(null, arguments), _.not(g.ctoken2("timeContext")));
    };
    g.day = _fn(g.d, g.dd);
    g.month = _fn(g.M, g.MMM);
    g.year = _fn(g.yyyy, g.yy);
    g.orientation = _.process(g.ctoken("past future"),
    function(s) {
        return function() {
            this.orient = s;
        };
    });
    g.operator = _.process(g.ctoken("add subtract"),
    function(s) {
        return function() {
            this.operator = s;
        };
    });
    g.rday = _.process(g.ctoken("yesterday tomorrow today now"), t.rday);
    g.unit = _.process(g.ctoken("minute hour day week month year"),
    function(s) {
        return function() {
            this.unit = s;
        };
    });
    g.value = _.process(_.rtoken(/^\d\d?(st|nd|rd|th)?/),
    function(s) {
        return function() {
            this.value = s.replace(/\D/g, "");
        };
    });
    g.expression = _.set([g.rday, g.operator, g.value, g.unit, g.orientation, g.ddd, g.MMM]);
    _fn = function() {
        return _.set(arguments, g.datePartDelimiter);
    };
    g.mdy = _fn(g.ddd, g.month, g.day, g.year);
    g.ymd = _fn(g.ddd, g.year, g.month, g.day);
    g.dmy = _fn(g.ddd, g.day, g.month, g.year);
    g.date = function(s) {
        return ((g[Date.CultureInfo.dateElementOrder] || g.mdy).call(this, s));
    };
    g.format = _.process(_.many(_.any(_.process(_.rtoken(/^(dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?)/),
    function(fmt) {
        if (g[fmt]) {
            return g[fmt];
        } else {
            throw Date.Parsing.Exception(fmt);
        }
    }), _.process(_.rtoken(/^[^dMyhHmstz]+/),
    function(s) {
        return _.ignore(_.stoken(s));
    }))),
    function(rules) {
        return _.process(_.each.apply(null, rules), t.finishExact);
    });
    var _F = {};
    var _get = function(f) {
        return _F[f] = (_F[f] || g.format(f)[0]);
    };
    g.formats = function(fx) {
        if (fx instanceof Array) {
            var rx = [];
            for (var i = 0; i < fx.length; i++) {
                rx.push(_get(fx[i]));
            }
            return _.any.apply(null, rx);
        } else {
            return _get(fx);
        }
    };
    g._formats = g.formats(["yyyy-MM-ddTHH:mm:ss", "ddd, MMM dd, yyyy H:mm:ss tt", "ddd MMM d yyyy HH:mm:ss zzz", "d"]);
    g._start = _.process(_.set([g.date, g.time, g.expression], g.generalDelimiter, g.whiteSpace), t.finish);
    g.start = function(s) {
        try {
            var r = g._formats.call({},
            s);
            if (r[1].length === 0) {
                return r;
            }
        } catch(e) {}
        return g._start.call({},
        s);
    };
} ());
Date._parse = Date.parse;
Date.parse = function(s) {
    var r = null;
    if (!s) {
        return null;
    }
    try {
        r = Date.Grammar.start.call({},
        s);
    } catch(e) {
        return null;
    }
    return ((r[1].length === 0) ? r[0] : null);
};
Date.getParseFunction = function(fx) {
    var fn = Date.Grammar.formats(fx);
    return function(s) {
        var r = null;
        try {
            r = fn.call({},
            s);
        } catch(e) {
            return null;
        }
        return ((r[1].length === 0) ? r[0] : null);
    };
};
Date.parseExact = function(s, fx) {
    return Date.getParseFunction(fx)(s);
};
$.datepicker.regional["de-DE"] = {
    closeText: "schlie&szlig;en",
    prevText: "&#x3c;zur&uuml;ck",
    nextText: "Vor&#x3e;",
    currentText: "heute",
    monthNames: ["Januar", "Februar", "M&auml;rz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
    monthNamesShort: ["Jan", "Feb", "M&auml;r", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
    dayNames: ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
    dayNamesShort: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
    dayNamesMin: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
    weekHeader: "Wo",
    dateFormat: "dd.mm.yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["en-CA"] = {
    closeText: "Done",
    prevText: "Prev",
    nextText: "Next",
    currentText: "Today",
    monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    weekHeader: "Wk",
    dateFormat: "dd/mm/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["en-GB"] = {
    closeText: "Done",
    prevText: "Prev",
    nextText: "Next",
    currentText: "Today",
    monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    weekHeader: "Wk",
    dateFormat: "dd/mm/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["en-IN"] = {
    closeText: "Done",
    prevText: "Prev",
    nextText: "Next",
    currentText: "Today",
    monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    weekHeader: "Wk",
    dateFormat: "d/m/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["en"] = {
    closeText: "Done",
    prevText: "Prev",
    nextText: "Next",
    currentText: "Today",
    monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    weekHeader: "Wk",
    dateFormat: "m/d/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["es"] = {
    closeText: "Cerrar",
    prevText: "&#x3c;Ant",
    nextText: "Sig&#x3e;",
    currentText: "Hoy",
    monthNames: ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    monthNamesShort: ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
    dayNames: ["domingo", "lunes", "martes", "mi&eacute;rcoles", "jueves", "viernes", "s&aacute;bado"],
    dayNamesShort: ["dom", "lun", "mar", "mi&eacute;", "jue", "vie", "s&aacute;b"],
    dayNamesMin: ["D", "L", "M", "X", "J", "V", "S"],
    weekHeader: "Sm",
    dateFormat: "d/mm/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["fr"] = {
    closeText: "Fermer",
    prevText: "&#x3c;Pr&eacute;c",
    nextText: "Suiv&#x3e;",
    currentText: "Courant",
    monthNames: ["Janvier", "F&eacute;vrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Ao&ucirc;t", "Septembre", "Octobre", "Novembre", "D&eacute;cembre"],
    monthNamesShort: ["Jan", "F&eacute;v", "Mar", "Avr", "Mai", "Jun", "Jul", "Ao&ucirc;", "Sep", "Oct", "Nov", "D&eacute;c"],
    dayNames: ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
    dayNamesShort: ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"],
    dayNamesMin: ["Di", "Lu", "Ma", "Me", "Je", "Ve", "Sa"],
    weekHeader: "Sm",
    dateFormat: "dd/mm/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["it"] = {
    closeText: "Chiudi",
    prevText: "&#x3c;Prec",
    nextText: "Succ&#x3e;",
    currentText: "Oggi",
    monthNames: ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"],
    monthNamesShort: ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"],
    dayNames: ["Domenica", "Luned&#236;", "Marted&#236;", "Mercoled&#236;", "Gioved&#236;", "Venerd&#236;", "Sabato"],
    dayNamesShort: ["Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab"],
    dayNamesMin: ["Do", "Lu", "Ma", "Me", "Gi", "Ve", "Sa"],
    weekHeader: "Sm",
    dateFormat: "dd/mm/yy",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
};
$.datepicker.regional["jp"] = {
    closeText: "&#38281;&#12376;&#12427;",
    prevText: "&#x3C;&#21069;",
    nextText: "&#27425;&#x3E;",
    currentText: "&#20170;&#26085;",
    monthNames: ["1&#26376;", "2&#26376;", "3&#26376;", "4&#26376;", "5&#26376;", "6&#26376;", "7&#26376;", "8&#26376;", "9&#26376;", "10&#26376;", "11&#26376;", "12&#26376;"],
    monthNamesShort: ["1&#26376;", "2&#26376;", "3&#26376;", "4&#26376;", "5&#26376;", "6&#26376;", "7&#26376;", "8&#26376;", "9&#26376;", "10&#26376;", "11&#26376;", "12&#26376;"],
    dayNames: ["&#26085;&#26332;&#26085;", "&#26376;&#26332;&#26085;", "&#28779;&#26332;&#26085;", "&#27700;&#26332;&#26085;", "&#26408;&#26332;&#26085;", "&#37329;&#26332;&#26085;", "&#22303;&#26332;&#26085;"],
    dayNamesShort: ["&#26085;", "&#26376;", "&#28779;", "&#27700;", "&#26408;", "&#37329;", "&#22303;"],
    dayNamesMin: ["&#26085;", "&#26376;", "&#28779;", "&#27700;", "&#26408;", "&#37329;", "&#22303;"],
    weekHeader: "&#36913;",
    dateFormat: "yy/mm/dd",
    firstDay: 0,
    isRTL: false,
    showMonthAfterYear: true,
    yearSuffix: "&#24180;"
};
$.datepicker.regional["zh-CN"] = {
    closeText: "&#20851;&#38381;",
    prevText: "&#x3C;&#19978;&#26376;",
    nextText: "&#19979;&#26376;&#x3E;",
    currentText: "&#20170;&#22825;",
    monthNames: ["&#19968;&#26376;", "&#20108;&#26376;", "&#19977;&#26376;", "&#22235;&#26376;", "&#20116;&#26376;", "&#20845;&#26376;", "&#19971;&#26376;", "&#20843;&#26376;", "&#20061;&#26376;", "&#21313;&#26376;", "&#21313;&#19968;&#26376;", "&#21313;&#20108;&#26376;"],
    monthNamesShort: ["&#19968;&#26376;", "&#20108;&#26376;", "&#19977;&#26376;", "&#22235;&#26376;", "&#20116;&#26376;", "&#20845;&#26376;", "&#19971;&#26376;", "&#20843;&#26376;", "&#20061;&#26376;", "&#21313;&#26376;", "&#21313;&#19968;&#26376;", "&#21313;&#20108;&#26376;"],
    dayNames: ["&#26143;&#26399;&#26085;", "&#26143;&#26399;&#19968;", "&#26143;&#26399;&#20108;", "&#26143;&#26399;&#19977;", "&#26143;&#26399;&#22235;", "&#26143;&#26399;&#20116;", "&#26143;&#26399;&#20845;"],
    dayNamesShort: ["&#21608;&#26085;", "&#21608;&#19968;", "&#21608;&#20108;", "&#21608;&#19977;", "&#21608;&#22235;", "&#21608;&#20116;", "&#21608;&#20845;"],
    dayNamesMin: ["&#26085;", "&#19968;", "&#20108;", "&#19977;", "&#22235;", "&#20116;", "&#20845;"],
    weekHeader: "&#21608;",
    dateFormat: "yy-m-d",
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: true,
    yearSuffix: "&#24180;"
}; (function($, undefined) {
    var maxFuture = (DRR.isFutureGenerationEnabled === "true") ? "+1y": -1;
    $.datepicker.setDefaults({
        minDate: (new Date(2012, 0, 1)),
        maxDate: maxFuture
    });
    var language = DRR.strings.datePickerLanguage;
    $.datepicker.setDefaults($.datepicker.regional[language]);
    $(".hasCal").datepicker();
    $(".drrreportpopuptrigger").amazonPopoverTrigger({
        localContent: "#drrReportRangePopover",
        width: 500,
        height: 500,
        draggable: true,
        closeEventExclude: "CLICK_OUTSIDE",
        title: DRR.strings.generateDateRangeReport,
        onShow: scFixPopoverStacking
    });
    $("#drrScheduleEndDate").datepicker("option", {
        minDate: 1,
        maxDate: null
    });
    var now = Date.today();
    $("option[value=" + now.getMonth() + "_" + now.getFullYear() + "]").attr("selected", "selected");
    function disableRecurrence() {
        $("#drrRecurrenceSettings").hide();
        $("#drrRepeatingReportGeneration").attr("disabled", "true");
        $("#drrRepeatingReportGeneration").attr("checked", false);
    }
    disableRecurrence();
    $("#drrReportRangeRadioCustom").click(function() {
        disableRecurrence();
    });
    $("#drrReportRangeYearAndMonth").change(function() {
        var curMonth = $("#drrReportRangeYearAndMonth").find(":selected").attr("class");
        if (curMonth == "future") {
            $("#drrRepeatingReportGeneration").removeAttr("disabled");
        } else {
            disableRecurrence();
        }
    });
    $("#drrRepeatingReportGeneration").click(function() {
        $("#drrRecurrenceSettings").toggle(this.checked);
    });
    $(".drrReportRangePopover select, .drrReportRangePopover input[type=text]").each(function() {
        $(this).change(function() {
            $this = $(this);
            $this.parent().find("input[type=radio]").click();
        });
    });
    function scFixPopoverStacking(popover, settings) {
        popover.parent().find("#ap_overlay, .ap_popover").css({
            zIndex: 2000
        });
    }
    $generateButton = $("button[name=Generate]");
    $generateButton.click(function() {
        generateReportAction();
    });
    $cancelButton = $("button[name=Cancel]");
    $cancelButton.click(function() {
        $("button[name=Generate]").show();
    });
    function generateReportAction() {
        var queryParams, $startDate, $endDate, $generationDate, $scheduledEndDate, $year, $month, $reportType, $scheduleTime, $quarter, $reportRecurrence, $rangeType = $("input[name=drrReportRange]:checked").attr("id").split("drrReportRangeRadio")[1];
        var validDay = new Date();
        if (DRR.isFutureGenerationEnabled === "true") {
            validDay.setFullYear(validDay.getFullYear + 1);
        } else {
            validDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        }
        var scheduledReport = false;
        $reportType = $("input[name=drrReportType]:checked");
        if ($reportType.length == 0) {
            alertPopover(DRR.strings.selectReportTypeValidation, null);
            return;
        } else {
            $reportType = $reportType.attr("id").split("drrReportTypeRadio")[1];
        }
        $reportRecurrence = $("input[name=drrReportRecurrence]:checked");
        if ($reportRecurrence.length != 0) {
            $yearAndMonth = $("#drrReportRangeYearAndMonth").val().split("_");
            $month = $yearAndMonth[0];
            $year = $yearAndMonth[1];
            if ($("#drrRecurrenceEndDate").is(":checked")) {
                $scheduledEndDate = $("#drrScheduleEndDate").datepicker("getDate");
                var $recurrenceEndDate = new Date($year, parseInt($month) - 1, 1);
                if (validateEmptyOrUndefined($scheduledEndDate)) {
                    reportRangeMssgWithDate(DRR.strings.selectValidRecurrenceEndDate, $recurrenceEndDate, null);
                    return;
                }
                if (($scheduledEndDate.getMonth() + 1 < $month) && ($scheduledEndDate.getFullYear() == $year)) {
                    reportRangeMssgWithDate(DRR.strings.selectValidRecurrenceEndDate, $recurrenceEndDate, null);
                    return;
                }
                if ($scheduledEndDate.getFullYear() < parseInt($year)) {
                    reportRangeMssgWithDate(DRR.strings.selectValidRecurrenceEndDate, $recurrenceEndDate, null);
                    return;
                }
            }
        }
        var $startDateDay, $startDateMonth, $startDateYear, $endDateDay, $endDateMonth, $endDateYear, $startDateTime, $endDateTime;
        if ($rangeType === "Monthly") {
            $yearAndMonth = $("#drrReportRangeYearAndMonth").val().split("_");
            $month = $yearAndMonth[0];
            $year = $yearAndMonth[1];
            if (validateEmptyOrUndefined($month) && validateEmptyOrUndefined($year) && validateEmptyOrUndefined($reportType)) {
                reportRangeError(DRR.strings.selectReportTypeValidation + "\n" + DRR.strings.selectMonthValidation + "\n" + DRR.strings.selectYearValidation);
                return;
            } else {
                if (validateEmptyOrUndefined($year) && validateEmptyOrUndefined($reportType)) {
                    reportRangeError(DRR.strings.selectReportTypeValidation + "\n" + DRR.strings.selectYearValidation);
                    return;
                } else {
                    if (validateEmptyOrUndefined($month) && validateEmptyOrUndefined($reportType)) {
                        reportRangeError(DRR.strings.selectReportTypeValidation + "\n" + DRR.strings.selectMonthValidation);
                        return;
                    } else {
                        if (validateEmptyOrUndefined($month) && validateEmptyOrUndefined($year)) {
                            reportRangeError(DRR.strings.selectYearValidation + "\n" + DRR.strings.selectMonthValidation);
                            return;
                        } else {
                            if (validateEmptyOrUndefined($year)) {
                                reportRangeError(DRR.strings.selectYearValidation);
                                return;
                            } else {
                                if (validateEmptyOrUndefined($month)) {
                                    reportRangeError(DRR.strings.selectMonthValidation);
                                    return;
                                } else {
                                    if (validateEmptyOrUndefined($reportType)) {
                                        reportRangeError(DRR.strings.selectReportTypeValidation);
                                        return;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            if ($year < 2012 || $year > (validDay.getFullYear())) {
                reportRangeError(DRR.strings.selectMonthInvalidMonthYear);
                return;
            }
            if ($year == validDay.getFullYear() && $month >= (validDay.getMonth() + 1)) {
                reportRangeError(DRR.strings.selectMonthInvalidMonthYear);
                return;
            }
            if ($month >= now.getMonth() + 1 && $year == now.getFullYear()) {
                scheduledReport = true;
            } else {
                if ($year > now.getFullYear()) {
                    scheduledReport = true;
                }
            }
            if (scheduledReport) {
                $generationDate = now;
                $generationDate.setMilliseconds(0);
                $generationDate.setDate(1);
                if ($month == 12) {
                    $generationDate.setMonth(0);
                    $generationDate.setFullYear(parseInt($year) + 1);
                } else {
                    $generationDate.setMonth(parseInt($month));
                    $generationDate.setFullYear($year);
                }
            }
        } else {
            if ($rangeType === "Yearly") {
                $year = $("#drrReportRangeYearly").val();
                if (validateEmptyOrUndefined($year)) {
                    reportRangeError(DRR.strings.selectYearValidation);
                    return;
                } else {
                    if (validateEmptyOrUndefined($reportType)) {
                        reportRangeError(DRR.strings.selectReportTypeValidation);
                        return;
                    }
                }
            } else {
                if ($rangeType === "Quarterly") {
                    $quarter = $("#drrReportRangeQuarterly").val();
                    $year = $("#drrReportRangeMonthly option:selected").attr("data-year");
                    if (validateEmptyOrUndefined($quarter)) {
                        reportRangeError(DRR.strings.selectQuarterValidation);
                        return;
                    } else {
                        if (validateEmptyOrUndefined($reportType)) {
                            reportRangeError(DRR.strings.selectReportTypeValidation);
                            return;
                        }
                    }
                } else {
                    if ($rangeType === "Custom") {
                        var startDateLimit = 1325289600;
                        $startDate = $("#drrReportStartDate").datepicker("getDate");
                        $endDate = $("#drrReportEndDate").datepicker("getDate");
                        if ((validateEmptyOrUndefined($startDate) || validateEmptyOrUndefined($endDate)) && validateEmptyOrUndefined($reportType)) {
                            reportRangeError(DRR.strings.selectReportTypeValidation + "\n" + DRR.strings.selectCustomDateRangeValidation);
                            return;
                        } else {
                            if (validateEmptyOrUndefined($startDate) || validateEmptyOrUndefined($endDate)) {
                                reportRangeError(DRR.strings.selectCustomDateRangeValidation);
                                return;
                            } else {
                                if (validateEmptyOrUndefined($reportType)) {
                                    reportRangeError(DRR.strings.selectReportTypeValidation);
                                    return;
                                }
                            }
                        }
                        $endDate.setHours(23);
                        $endDate.setMinutes(59);
                        $endDate.setSeconds(59);
                        if (isNaN($startDate) || isNaN($endDate)) {
                            reportRangeError(DRR.strings.selectCustomValidDateRangeInvalidDate);
                            return;
                        }
                        if (!validateDate($startDate) || !validateDate($endDate)) {
                            reportRangeError(DRR.strings.selectCustomValidDateRangeInvalidDate);
                            return;
                        }
                        if (($endDate >= validDay) || (($startDate.getTime() / 1000) < startDateLimit) || ($startDate > $endDate)) {
                            reportRangeError(DRR.strings.selectCustomValidDateRangeInvalidRange);
                            return;
                        }
                        $startDateDay = $startDate.getDate();
                        $startDateMonth = $startDate.getMonth() + 1;
                        $startDateYear = $startDate.getFullYear();
                        $endDateDay = $endDate.getDate();
                        $endDateMonth = $endDate.getMonth() + 1;
                        $endDateYear = $endDate.getFullYear();
                        $startDateTime = $startDate.getTime() / 1000;
                        $endDateTime = $endDate.getTime() / 1000;
                        var yesterday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
                        if ($startDate > yesterday || $endDate > yesterday) {
                            scheduledReport = true;
                        }
                        if (scheduledReport) {
                            $generationDate = $endDate.add(1).days();
                            $generationDate.setSeconds(now.getSeconds());
                            $generationDate.setMinutes(now.getMinutes());
                            $generationDate.setHours(now.getHours());
                        }
                    }
                }
            }
        }
        $("button[name=Generate]").hide();
        $("button[name=Cancel]").hide();
        var parameters = {
            startDate: $startDateTime,
            endDate: $endDateTime,
            month: $month,
            year: $year,
            timeRangeType: $rangeType,
            quarter: $quarter,
            reportType: $reportType,
            startDateDay: $startDateDay,
            startDateMonth: $startDateMonth,
            startDateYear: $startDateYear,
            endDateDay: $endDateDay,
            endDateMonth: $endDateMonth,
            endDateYear: $endDateYear,
        };
        var $generationDatePersist = $generationDate;
        if ($generationDate) {
            $generationDate = $generationDate.getTime() / 1000;
            parameters["generationDate"] = $generationDate;
        }
        if ($reportRecurrence.length != 0) {
            parameters["isRecurring"] = true;
        }
        if ($scheduledEndDate) {
            $scheduledEndDate = $scheduledEndDate.getTime() / 1000;
            parameters["scheduledEndDate"] = $scheduledEndDate;
        }
        if (scheduledReport) {
            reportRangeMssgWithDate(DRR.strings.reportScheduleStarted, $generationDatePersist, parameters);
        } else {
            if ($reportRecurrence.length != 0) {
                reportRangeMssgWithDate(DRR.strings.reportRecurrenceStarted, $generationDatePersist, parameters);
            } else {
                alertPopover(DRR.strings.reportGenerationStarted, parameters);
            }
        }
    }
    function validateEmptyOrUndefined(stringContent) {
        if (stringContent === "" || stringContent == undefined) {
            return true;
        }
        return false;
    }
    function validateDate(date) {
        re = /^\d{1,2}\/\d{1,2}\/\d{4}$/;
        var dateFormat = date.getMonth() + "/" + date.getDate() + "/" + date.getFullYear();
        if (!dateFormat.match(re)) {
            return false;
        }
        return true;
    }
    function reportRangeError(error) {
        alertPopover(error, null);
    }
    function reportRangeMssgWithDate(message, date, parameters) {
        $("#drrScheduleEndDate").datepicker("setDate", new Date(date));
        alertPopover(message + " " + $("#drrScheduleEndDate").val(), parameters);
        $("#drrScheduleEndDate").datepicker("setDate", "");
    }
    function alertPopover(message, parameters) {
        var popoverParams = {
            width: 350,
            position: "over",
            modal: true,
            closeEventExclude: ["CLICK_OUTSIDE"],
            literalContent: "<div style='text-align=center;'><p>" + message + "</p><p align='center'><button type='button' onclick='#close' class='ap_custom_close'>OK</button></p></div>"
        };
        if (null != parameters) {
            popoverParams["onHide"] = function() {
                jQuery.post("/gp/payments-account/generate-date-range-report.html", parameters,
                function(data) {
                    window.location.reload();
                });
            };
        }
        jQuery.AmazonPopover.displayPopover(popoverParams);
    }
})(jQuery);
amznJQ.declareAvailable("date-range-report-popup"); (function() {
    function QueryString(qs) {
        this.dict = {};
        if (!qs) {
            qs = location.search;
        }
        if (qs.charAt(0) == "?") {
            qs = qs.substring(1);
        }
        var re = /([^=&]+)(=([^&]*))?/g;
        while (match = re.exec(qs)) {
            var key = decodeURIComponent(match[1].replace(/\+/g, " "));
            var value = match[3] ? QueryString.decode(match[3]) : "";
            if (this.dict[key]) {
                this.dict[key].push(value);
            } else {
                this.dict[key] = [value];
            }
        }
    }
    QueryString.decode = function(s) {
        s = s.replace(/\+/g, " ");
        s = s.replace(/%([EF][0-9A-F])%([89AB][0-9A-F])%([89AB][0-9A-F])/g,
        function(code, hex1, hex2, hex3) {
            var n1 = parseInt(hex1, 16) - 224;
            var n2 = parseInt(hex2, 16) - 128;
            if (n1 === 0 && n2 < 32) {
                return code;
            }
            var n3 = parseInt(hex3, 16) - 128;
            var n = (n1 << 12) + (n2 << 6) + n3;
            if (n > 65535) {
                return code;
            }
            return String.fromCharCode(n);
        });
        s = s.replace(/%([CD][0-9A-F])%([89AB][0-9A-F])/g,
        function(code, hex1, hex2) {
            var n1 = parseInt(hex1, 16) - 192;
            if (n1 < 2) {
                return code;
            }
            var n2 = parseInt(hex2, 16) - 128;
            return String.fromCharCode((n1 << 6) + n2);
        });
        s = s.replace(/%([0-7][0-9A-F])/g,
        function(code, hex) {
            return String.fromCharCode(parseInt(hex, 16));
        });
        return s;
    };
    QueryString.prototype.value = function(key) {
        var a = this.dict[key];
        return a ? a[a.length - 1] : undefined;
    };
    QueryString.prototype.values = function(key) {
        var a = this.dict[key];
        return a ? a: [];
    };
    QueryString.prototype.keys = function() {
        var a = [];
        for (var key in this.dict) {
            a.push(key);
        }
        return a;
    };
    QueryString.prototype.add = function(key, value) {
        if (this.dict[key]) {
            this.dict[key].push(value);
        } else {
            this.dict[key] = [value];
        }
        return this.dict[key];
    };
    QueryString.prototype.set = function(key, value) {
        this.dict[key] = value;
        return this.dict[key];
    };
    QueryString.prototype.toString = function() {
        var str = [];
        for (var p in this.dict) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(this.dict[p]));
        }
        return str.join("&");
    };
    var DRR = window.DRR || {};
    DRR.qs = new QueryString();
})(); (function($, undefined) {
    $.fn.selectText = function() {
        var d = document,
        elem = this.get(0);
        if (d.body.createTextRange) {
            var range = d.body.createTextRange();
            range.moveToElementText(elem);
            range.select();
        } else {
            if (window.getSelection) {
                var selection = window.getSelection(),
                range = d.createRange();
                range.selectNodeContents(elem);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        }
        return this;
    };
    var DRR = window.DRR || {};
    var $head, $wrapper, $filters, $bits, $tab, $content, $sortMenu, $tables;
    var $openMenu, $filterBars = $(),
    data = [],
    types = [],
    years = {},
    currentSort;
    var activeFilters = [];
    function init() {
        $head = $("#drrPageHeader");
        $wrapper = $("#drrWrapper");
        $filters = $("#drrFilters");
        $bits = $("#drrFilterSidebarBits");
        $tab = $("#drrFilterTab");
        $content = $("#drrContent");
        $sortMenu = $("#drrSortDropdown");
        $tables = $content.find("table.drrDocumentGroupTable");
        var $filterBar = $bits.find("div.drrDocumentGroupFilters").detach(),
        $filterBarClone;
        onResizeWindow();
        currentSort = "default";
        $("#sc_footer_container").detach().appendTo($content);
        if ($.browser.msie && parseInt($.browser.version.slice(0, 3)) < 9) {
            $("html").addClass("ieLow");
            $tab.css("filter", "progid:DXImageTransform.Microsoft.Matrix(M11=6.123233995736766e-17, M12=-1, M21=1, M22=6.123233995736766e-17, sizingMethod='auto expand')");
        }
        $wrapper.addClass("drrWrapperWithFilters drrUnlocked");
        $tables.each(function(iTable) {
            var $table = $(this).children("tbody");
            $table.data("index", iTable);
            $filterBarClone = $filterBar.clone();
            $table.closest("table").before($filterBarClone);
            $filterBars = $filterBars.add($filterBarClone);
            data[iTable] = [];
            $table.find("tr").each(function(iRow) {
                var $row = $(this);
                $row.find("td").each(function(iCol) {
                    if (data[iTable][iCol] === undefined) {
                        data[iTable][iCol] = [];
                    }
                    var $this = $(this),
                    sortDate = $this.attr("data-sort-date"),
                    sortVal;
                    if (sortDate) {
                        sortVal = sortDate;
                    } else {
                        sortVal = $this.text();
                    }
                    data[iTable][iCol][iRow] = {
                        $row: $row,
                        val: sortVal
                    };
                });
            });
        });
        for (var iTable = 0,
        lTable = data.length; iTable < lTable; iTable++) {
            types[iTable] = {};
            activeFilters[iTable] = 0;
            for (var iRow = 0,
            lRow = data[iTable][0].length; iRow < lRow; iRow++) {
                var $row = data[iTable][0][iRow].$row,
                name = $row.attr("data-type"),
                year = $row.attr("data-year");
                if (name !== undefined) {
                    if (!types[iTable][name]) {
                        types[iTable][name] = {
                            count: 0,
                            $rows: $(),
                            $bubbles: $(),
                            $filter: $()
                        };
                    }
                    types[iTable][name].count++;
                    types[iTable][name].$rows = types[iTable][name].$rows.add($row);
                }
                if (year !== undefined) {
                    if (year !== undefined && !years[year]) {
                        years[year] = {
                            count: 0,
                            $rows: $(),
                            $bubbles: $(),
                            $filter: $()
                        };
                    }
                    years[year].count++;
                    years[year].$rows = years[year].$rows.add($row);
                }
                $row.data("activeFilters", 0);
            }
        }
        var $group = $bits.children("div.drrFilterGroup"),
        $li = $group.find("li").detach(),
        $groupClone = $group.clone(),
        $liClone,
        $bubble = $bits.children("span.drrFilterBubble"),
        $bubbleClone,
        keys = [];
        if (years.length) {
            setFilterGroupTitle($groupClone, "Year");
            for (year in years) {
                keys.push(year);
            }
            keys.sort();
            for (var iYear = 0,
            lYear = keys.length; iYear < lYear; iYear++) {
                $liClone = $li.clone();
                $liClone.data("year", keys[iYear]).children(".drrFilterType").text(keys[iYear]).end().children(".drrFilterCount").text(years[keys[iYear]].count);
                $groupClone.find("ul.drrFilterGroupList").append($liClone);
                years[keys[iYear]].$filter = $liClone;
                $bubbleClone = $bubble.clone();
                $bubbleClone.data("year", keys[iYear]).children(".drrFilterType").text(keys[iYear]);
                $filterBars.each(function() {
                    var $cloneClone = $bubbleClone.clone(true),
                    $this = $(this);
                    $this.append($cloneClone);
                    years[keys[iYear]].$bubbles = years[keys[iYear]].$bubbles.add($cloneClone);
                });
            }
            $filters.append($groupClone);
        }
        for (var iTable = 0,
        lTable = types.length; iTable < lTable; iTable++) {
            $groupClone = $group.clone();
            var groupTitle = $tables.eq(iTable).attr("data-filter-title");
            setFilterGroupTitle($groupClone, groupTitle);
            keys = [];
            for (type in types[iTable]) {
                keys.push(type);
            }
            keys.sort();
            for (var iType = 0,
            lType = keys.length; iType < lType; iType++) {
                $liClone = $li.clone();
                $liClone.data("type", keys[iType]).data("table", iTable).children(".drrFilterType").text(keys[iType]).end().children(".drrFilterCount").text(types[iTable][keys[iType]].count);
                $groupClone.find("ul.drrFilterGroupList").append($liClone);
                types[iTable][keys[iType]].$filter = $liClone;
                $bubbleClone = $bubble.clone();
                $bubbleClone.data("type", keys[iType]).data("table", iTable).children(".drrFilterType").text(keys[iType]);
                $filterBars.eq(iTable).append($bubbleClone);
                types[iTable][keys[iType]].$bubbles = types[iTable][keys[iType]].$bubbles.add($bubbleClone);
            }
            $filters.append($groupClone);
        }
        function setFilterGroupTitle($group, title) {
            $group.children("div.drrFilterGroupHeader").children(".drrFilterGroupTitle").text(title);
        }
        $(window).resize(onResizeWindow);
        $("html").click(onHtmlClick);
        $content.delegate("th", "click", onClickTableHeader);
        $sortMenu.delegate("li", "click", onClickSortMenu);
        $tab.click(onClickFilterTab);
        $filters.delegate("div.drrFilterGroupHeader", "click", onClickFilterGroup).delegate("ul.drrFilterGroupList li", "click", onClickFilter);
        $content.delegate("span.drrRemoveAllFilters", "click", onClickFilterBarClose).delegate("span.drrFilterBubble", "click", onClickFilterBubble);
        if (DRR.qs.keys().length > 0) {
            applyQueryParams();
        }
    }
    function onResizeWindow() {
        var $spooferBar = $("#spooferDiv");
        var top;
        if ($spooferBar.length && $wrapper.hasClass("drrWrapperWithFilters")) {
            top = $spooferBar.outerHeight() + $head.outerHeight() + "px";
        } else {
            top = $head.outerHeight() + "px";
        }
        $wrapper.css("top", top);
    }
    function onClickPassphraseBox() {
        $(this).selectText();
    }
    function onHtmlClick() {
        hideDropdown();
    }
    function onClickFilterTab() {
        $wrapper.toggleClass("drrUnlocked");
    }
    function onClickFilterGroup() {
        var $this = $(this);
        $this.find("span.drrFilterGroupArrow").toggleClass("drrFilterGroupArrowCollapsed");
        $this.siblings("ul.drrFilterGroupList").toggle();
    }
    function onClickFilter(e) {
        var $this = $(this),
        selected = $this.hasClass("drrFilterSelected"),
        isYear,
        key,
        table;
        if (key = $this.data("year")) {
            isYear = true;
        } else {
            isYear = false;
            key = $this.data("type");
            table = $this.data("table");
        }
        $this.toggleClass("drrFilterSelected").find(".drrFilterX").toggle();
        var counterAdjust = (selected) ? -1 : 1,
        showOrHide = !selected;
        if (isYear) {
            for (var i = 0,
            l = activeFilters.length; i < l; i++) {
                if (activeFilters[i] === 0) {
                    $tables.eq(i).find("tbody tr").hide();
                    $filterBars.eq(i).show();
                }
                activeFilters[i] += counterAdjust;
            }
            years[key].$bubbles.toggle(showOrHide);
            years[key].$rows.each(function() {
                $row = $(this);
                $row.data().activeFilters += counterAdjust;
                $row.toggle($row.data().activeFilters !== 0);
            });
            for (var i = 0,
            l = activeFilters.length; i < l; i++) {
                if (activeFilters[i] === 0) {
                    $tables.eq(i).find("tbody tr").show();
                    $filterBars.eq(i).hide();
                }
            }
        } else {
            if (activeFilters[table] === 0) {
                $tables.eq(table).find("tbody tr").hide();
                $filterBars.eq(table).show();
            }
            activeFilters[table] += counterAdjust;
            types[table][key].$bubbles.toggle(showOrHide);
            types[table][key].$rows.each(function() {
                $row = $(this);
                $row.data().activeFilters += counterAdjust;
                $row.toggle($row.data().activeFilters !== 0);
            });
            if (activeFilters[table] === 0) {
                $tables.eq(table).find("tbody tr").show();
                $filterBars.eq(table).hide();
            }
        }
    }
    function onClickFilterBubble() {
        var $this = $(this),
        key;
        if (key = $this.data("year")) {
            years[key].$filter.click();
        } else {
            var table = $this.data("table");
            key = $this.data("type");
            types[table][key].$filter.click();
        }
    }
    function onClickFilterBarClose() {
        $(this).siblings("span.drrFilterBubble:visible").click();
        $(this).closest("div.drrDocumentGroupFilters").hide();
    }
    function onClickTableHeader(e) {
        var $this = $(this),
        $menu = ($this.hasClass("drrCol1")) ? $selectMenu: $sortMenu,
        $target = $(e.target);
        if ($target.is("input") || $target.hasClass("drrCol2") || $target.hasClass("drrCol6")) {
            return;
        }
        if ($this.hasClass("drrMenuOpen")) {
            hideDropdown();
        } else {
            displayDropdown($this, $menu);
        }
        e.stopPropagation();
    }
    function onClickSortMenu() {
        var $this = $(this),
        $th = $this.closest("th"),
        value = $this.attr("data-value"),
        tableIndex = $th.closest("thead").siblings().data("index"),
        colIndex = $th.prevAll("th").length;
        if (value == 0) {
            sortTable(tableIndex, colIndex);
        } else {
            if (value == 1) {
                sortTable(tableIndex, colIndex, true);
            }
        }
    }
    function displayDropdown($th, $menu) {
        hideDropdown();
        var $positioner = findPositioner();
        if (!$positioner.length) {
            var html = '<div class="drrMenuPositioner">&nbsp;<span class="drrMenuAnchor">' + $th.html() + "</span></div>";
            $th.html(html);
            $positioner = findPositioner();
        }
        var $menuAnchor = $positioner.find("span.drrMenuAnchor"),
        top = $menuAnchor.outerHeight() - 1,
        minWidth = $menuAnchor.outerWidth() + 5;
        $menu.css({
            "top": top + "px",
            "min-width": minWidth + "px"
        });
        $menu.detach().appendTo($positioner);
        $th.addClass("drrMenuOpen");
        $menu.show();
        $openMenu = $th;
        function findPositioner() {
            return $th.find("div.drrMenuPositioner");
        }
    }
    function hideDropdown() {
        if ($openMenu) {
            $openMenu.removeClass("drrMenuOpen");
            $openMenu.find("ul.drrDropdown").hide();
            $openMenu = false;
        }
    }
    function sortTable(tableIndex, colIndex, descending) {
        var arr = data[tableIndex][colIndex].slice(),
        $table = $tables.eq(tableIndex).children("tbody");
        if (colIndex === 1 || colIndex === 2) {
            arr.sort(compareDate);
        } else {
            arr.sort(compareString);
        }
        if (descending) {
            for (var i = 0,
            iLen = arr.length; i < iLen; i++) {
                arr[i].$row.detach().prependTo($table);
            }
        } else {
            for (var i = 0,
            iLen = arr.length; i < iLen; i++) {
                arr[i].$row.detach().appendTo($table);
            }
        }
        setCurrentSort(colIndex, descending);
        function setCurrentSort(colIndex, descending) {
            var direction = (descending) ? "DESC": "ASC";
            currentSort = {
                colIndex: colIndex,
                direction: direction
            };
        }
        function compareString(a, b) {
            var aString = a.val,
            bString = b.val;
            if (aString < bString) {
                return - 1;
            } else {
                if (aString > bString) {
                    return 1;
                } else {
                    return 0;
                }
            }
        }
        function compareDate(a, b) {
            var aDate = new Date(a.val),
            bDate = new Date(b.val);
            if (aDate < bDate) {
                return - 1;
            } else {
                if (aDate > bDate) {
                    return 1;
                } else {
                    return 0;
                }
            }
        }
    }
    function getActiveFilters() {
        var filters = [];
        $(".drrDocumentGroupFilters").find(".drrFilterType:visible").each(function(i, f) {
            filters.push($(f).text());
        });
        return filters.join(",");
    }
    function getVisibleCount() {
        return $(".drrDocumentGroupTable").find("tbody").find("tr:visible").length;
    }
    function getCurrentSort() {
        return currentSort;
    }
    function applyFilter(type) {
        type = type.split(",");
        for (var i = type.length - 1; i >= 0; i--) {
            if (!types[0][type[i]]) {
                throw new Error("Filter Type does not exist!");
            } else {
                types[0][type[i]].$filter.click();
            }
        }
        $tab.click();
    }
    function applyCurrentSort(colIndex, direction) {
        var descending = (direction == "DESC") ? true: undefined;
        sortTable(0, colIndex, descending);
    }
    function applyQueryParams() {
        if (DRR.qs.value("activeFilters")) {}
        if (DRR.qs.value("colIndex")) {
            applyCurrentSort(DRR.qs.value("colIndex"), DRR.qs.value("direction") ? DRR.qs.value("direction") : "DESC");
        }
    }
    function refreshWithParams(token, x, y) {
        token = token || "";
        x = x || "";
        y = y || "";
        var sort = getCurrentSort();
        if (sort !== "default") {
            DRR.qs.set("colIndex", sort.colIndex);
            DRR.qs.set("direction", sort.direction);
        } else {
            DRR.qs.set("colIndex", 1);
            DRR.qs.set("direction", "ASC");
        }
        DRR.qs.set("token", token);
        DRR.qs.set("x", x);
        DRR.qs.set("y", y);
        var newPage = "?" + DRR.qs.toString();
        window.location.replace(newPage);
        return false;
    }
    DRR.init = init;
    DRR.getActiveFilters = getActiveFilters;
    DRR.getCurrentSort = getCurrentSort;
    DRR.getVisibleCount = getVisibleCount;
    DRR.applyFilter = applyFilter;
    DRR.applyCurrentSort = applyCurrentSort;
    DRR.applyQueryParams = applyQueryParams;
    DRR.refreshWithParams = refreshWithParams;
    DRR.cache = {
        data: data,
        types: types,
        years: years
    };
    window.DRR = DRR;
})(jQuery);
amznJQ.declareAvailable("date-range-report");
jQuery(document).ready(function() {
    jQuery(".regenerateDateRangeButton").click(function() {
        jQuery(this).replaceWith(jQuery(".progressText").html());
        jQuery.post("/gp/payments-account/generate-date-range-report.html", {
            reportRequestId: jQuery(this).attr("reportRequestId"),
            startDate: jQuery(this).attr("startDate"),
            endDate: jQuery(this).attr("endDate"),
            month: jQuery(this).attr("month"),
            year: jQuery(this).attr("year"),
            timeRangeType: jQuery(this).attr("timeRangeType"),
            reportType: jQuery(this).attr("reportType")
        });
    });
    jQuery(".cancelDateRangeLink").click(function() {
        jQuery("#" + jQuery(this).attr("reportRequestId")).replaceWith(jQuery(".cancelledText").html());
        jQuery.post("/gp/payments-account/generate-date-range-report.html", {
            reportRequestId: jQuery(this).attr("reportRequestId"),
            startDate: jQuery(this).attr("startDate"),
            endDate: jQuery(this).attr("endDate"),
            month: jQuery(this).attr("month"),
            year: jQuery(this).attr("year"),
            timeRangeType: jQuery(this).attr("timeRangeType"),
            reportType: jQuery(this).attr("reportType"),
            rgfPublishingLogId: jQuery(this).attr("rgfPublishingLogId"),
            requestAction: "Cancel",
        });
    });
});