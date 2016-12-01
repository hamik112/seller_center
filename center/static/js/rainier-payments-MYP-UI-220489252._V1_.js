function initializeCalendar(spec) {
    var monthNames, currentDateField, dateFormat, cal;
    monthNames = spec.monthNames;
    dateFormat = spec.dateFormat;
    currentDateField = "";
    cal = new CalendarPopup("calPopDiv");
    cal.setDateFormat(dateFormat);
    cal.setMonthNames.apply(cal, monthNames);
    cal.setDayHeaders("S", "M", "T", "W", "T", "F", "S");
    cal.showTodayLink = false;
    cal.showYearNavigation();
    window.gMonthNamesArray = monthNames;
    window.gCurrentDateField = currentDateField;
    window.cal = cal;
    addCalendarStyle();
}
function addCalendarStyle() {
    $(document.body).append(getCalendarStyles());
}
function CalendarPopup() {
    var c;
    if (arguments.length > 0) {
        c = new PopupWindow(arguments[0]);
    } else {
        c = new PopupWindow();
        c.setSize(150, 175);
    }
    c.offsetX = -152;
    c.offsetY = 25;
    c.autoHide();
    c.monthNames = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
    c.monthAbbreviations = new Array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
    c.dayHeaders = new Array("S", "M", "T", "W", "T", "F", "S");
    c.returnFunction = "CP_tmpReturnFunction";
    c.returnMonthFunction = "CP_tmpReturnMonthFunction";
    c.returnQuarterFunction = "CP_tmpReturnQuarterFunction";
    c.returnYearFunction = "CP_tmpReturnYearFunction";
    c.weekStartDay = 0;
    c.isShowYearNavigation = false;
    c.displayType = "date";
    c.disabledWeekDays = new Object();
    c.disabledDatesExpression = "";
    c.yearSelectStartOffset = 2;
    c.currentDate = null;
    c.showTodayLink = true;
    c.todayText = "Today";
    c.defaultSelectToday = false;
    c.cssPrefix = "";
    c.dateFormat = "";
    c.isShowNavigationDropdowns = false;
    c.isShowYearNavigationInput = false;
    window.CP_calendarObject = null;
    window.CP_targetInput = null;
    window.CP_dateFormat = "MM/dd/yyyy";
    c.copyMonthNamesToWindow = CP_copyMonthNamesToWindow;
    c.setReturnFunction = CP_setReturnFunction;
    c.setReturnMonthFunction = CP_setReturnMonthFunction;
    c.setReturnQuarterFunction = CP_setReturnQuarterFunction;
    c.setReturnYearFunction = CP_setReturnYearFunction;
    c.setMonthNames = CP_setMonthNames;
    c.setMonthAbbreviations = CP_setMonthAbbreviations;
    c.setDayHeaders = CP_setDayHeaders;
    c.setWeekStartDay = CP_setWeekStartDay;
    c.setDisplayType = CP_setDisplayType;
    c.setDisabledWeekDays = CP_setDisabledWeekDays;
    c.clearDisabledDates = CP_clearDisabledDates;
    c.addDisabledDates = CP_addDisabledDates;
    c.setYearSelectStartOffset = CP_setYearSelectStartOffset;
    c.setTodayText = CP_setTodayText;
    c.showYearNavigation = CP_showYearNavigation;
    c.showCalendar = CP_showCalendar;
    c.hideCalendar = CP_hideCalendar;
    c.getStyles = getCalendarStyles;
    c.refreshCalendar = CP_refreshCalendar;
    c.getCalendar = CP_getCalendar;
    c.select = CP_select;
    c.setCssPrefix = CP_setCssPrefix;
    c.setDateFormat = CP_setDateFormat;
    c.showNavigationDropdowns = CP_showNavigationDropdowns;
    c.showYearNavigationInput = CP_showYearNavigationInput;
    c.copyMonthNamesToWindow();
    return c;
}
function CP_copyMonthNamesToWindow() {
    if (typeof(window.MONTH_NAMES) != "undefined" && window.MONTH_NAMES != null) {
        window.MONTH_NAMES = new Array();
        for (var i = 0; i < this.monthNames.length; i++) {
            window.MONTH_NAMES[window.MONTH_NAMES.length] = this.monthNames[i];
        }
        for (var i = 0; i < this.monthAbbreviations.length; i++) {
            window.MONTH_NAMES[window.MONTH_NAMES.length] = this.monthAbbreviations[i];
        }
    }
}
function CP_tmpReturnFunction(y, m, d) {
    if (window.CP_targetInput != null) {
        var dt = new Date(y, m - 1, d, 0, 0, 0);
        if (window.CP_calendarObject != null) {
            window.CP_calendarObject.copyMonthNamesToWindow();
        }
        window.CP_targetInput.value = formatDate(dt, window.CP_dateFormat);
    } else {
        alert("Use setReturnFunction() to define which function will get the clicked results!");
    }
}
function CP_tmpReturnMonthFunction(y, m) {
    alert("Use setReturnMonthFunction() to define which function will get the clicked results!\nYou clicked: year=" + y + " , month=" + m);
}
function CP_tmpReturnQuarterFunction(y, q) {
    alert("Use setReturnQuarterFunction() to define which function will get the clicked results!\nYou clicked: year=" + y + " , quarter=" + q);
}
function CP_tmpReturnYearFunction(y) {
    alert("Use setReturnYearFunction() to define which function will get the clicked results!\nYou clicked: year=" + y);
}
function CP_setReturnFunction(name) {
    this.returnFunction = name;
}
function CP_setReturnMonthFunction(name) {
    this.returnMonthFunction = name;
}
function CP_setReturnQuarterFunction(name) {
    this.returnQuarterFunction = name;
}
function CP_setReturnYearFunction(name) {
    this.returnYearFunction = name;
}
function CP_setMonthNames() {
    for (var i = 0; i < arguments.length; i++) {
        this.monthNames[i] = arguments[i];
    }
    this.copyMonthNamesToWindow();
}
function CP_setMonthAbbreviations() {
    for (var i = 0; i < arguments.length; i++) {
        this.monthAbbreviations[i] = arguments[i];
    }
    this.copyMonthNamesToWindow();
}
function CP_setDayHeaders() {
    for (var i = 0; i < arguments.length; i++) {
        this.dayHeaders[i] = arguments[i];
    }
}
function CP_setWeekStartDay(day) {
    this.weekStartDay = day;
}
function CP_showYearNavigation() {
    this.isShowYearNavigation = (arguments.length > 0) ? arguments[0] : true;
}
function CP_setDisplayType(type) {
    if (type != "date" && type != "day" && type != "week-end" && type != "month" && type != "quarter" && type != "year") {
        alert("Invalid display type! Must be one of: date,week-end,month,quarter,year");
        return false;
    }
    if (type == "day") {
        type = "date";
    }
    this.displayType = type;
}
function CP_setYearSelectStartOffset(num) {
    this.yearSelectStartOffset = num;
}
function CP_setDisabledWeekDays() {
    this.disabledWeekDays = new Object();
    for (var i = 0; i < arguments.length; i++) {
        this.disabledWeekDays[arguments[i]] = true;
    }
}
function CP_clearDisabledDates() {
    this.disabledDatesExpression = "";
}
function CP_addDisabledDates(start, end) {
    if (arguments.length == 1) {
        end = start;
    }
    if (start == null && end == null) {
        return;
    }
    if (this.disabledDatesExpression != "") {
        this.disabledDatesExpression += "||";
    }
    if (start != null) {
        start = "" + start.getFullYear() + LZ(start.getMonth() + 1) + LZ(start.getDate());
    }
    if (end != null) {
        end = "" + end.getFullYear() + LZ(end.getMonth() + 1) + LZ(end.getDate());
    }
    if (start == null) {
        this.disabledDatesExpression += "(ds<=" + end + ")";
    } else {
        if (end == null) {
            this.disabledDatesExpression += "(ds>=" + start + ")";
        } else {
            this.disabledDatesExpression += "(ds>=" + start + "&&ds<=" + end + ")";
        }
    }
}
function CP_setTodayText(text) {
    this.todayText = text;
}
function CP_setCssPrefix(val) {
    this.cssPrefix = val;
}
function CP_setDateFormat(val) {
    this.dateFormat = val;
}
function CP_showNavigationDropdowns() {
    this.isShowNavigationDropdowns = (arguments.length > 0) ? arguments[0] : true;
}
function CP_showYearNavigationInput() {
    this.isShowYearNavigationInput = (arguments.length > 0) ? arguments[0] : true;
}
function CP_hideCalendar() {
    if (arguments.length > 0) {
        window.popupWindowObjects[arguments[0]].hidePopup();
    } else {
        this.hidePopup();
    }
}
function CP_refreshCalendar(index) {
    var calObject = window.popupWindowObjects[index];
    if (arguments.length > 1) {
        calObject.populate(calObject.getCalendar(arguments[1], arguments[2], arguments[3], arguments[4], arguments[5]));
    } else {
        calObject.populate(calObject.getCalendar());
    }
    calObject.refresh();
}
function CP_showCalendar(anchorname) {
    if (arguments.length > 1) {
        if (arguments[1] == null || arguments[1] == "") {
            this.currentDate = new Date();
        } else {
            this.currentDate = new Date(parseDate(arguments[1]));
        }
    }
    this.populate(this.getCalendar());
    this.showPopup(anchorname);
}
function CP_select(inputobj, linkname, format) {
    var selectedDate = (arguments.length > 3) ? arguments[3] : null;
    if (!window.getDateFromFormat) {
        alert("calendar.select: To use this method you must also include 'date.js' for date formatting");
        return;
    }
    if (this.displayType != "date" && this.displayType != "week-end") {
        alert("calendar.select: This function can only be used with displayType 'date' or 'week-end'");
        return;
    }
    if (inputobj.type != "text" && inputobj.type != "hidden" && inputobj.type != "textarea") {
        alert("calendar.select: Input object passed is not a valid form input object");
        window.CP_targetInput = null;
        return;
    }
    if (inputobj.disabled) {
        return;
    }
    window.CP_targetInput = inputobj;
    window.CP_calendarObject = this;
    this.currentDate = null;
    var time = 0;
    if (inputobj.value != "") {
        time = getDateFromFormat(inputobj.value, format ? format: this.dateFormat);
    }
    if (time == null && selectedDate != null) {
        time = getDateFromFormat(selectedDate, format ? format: this.dateFormat);
    }
    if (selectedDate != null || inputobj.value != "") {
        if (time == 0 || time == null) {
            this.currentDate = null;
        } else {
            this.currentDate = new Date(time);
        }
    }
    window.CP_dateFormat = format ? format: this.dateFormat;
    this.showCalendar(linkname);
}
function getCalendarStyles() {
    var result = "";
    var p = "";
    if (this != null && typeof(this.cssPrefix) != "undefined" && this.cssPrefix != null && this.cssPrefix != "") {
        p = this.cssPrefix;
    }
    result += "<STYLE>\n";
    result += "." + p + "cpYearNavigation,A." + p + "cpYearNavigation,A:visited." + p + "cpYearNavigation,." + p + "cpMonthNavigation,A." + p + "cpMonthNavigation,A:visited." + p + "cpMonthNavigation { background-color:#eeeeee; text-align:center; vertical-align:center; text-decoration:none; color:#000000; }\n";
    result += "." + p + "cpDayColumnHeader, ." + p + "cpYearNavigation,." + p + "cpMonthNavigation,A." + p + "cpMonthNavigation,A:visited." + p + "cpMonthNavigation,." + p + "cpCurrentMonthDate,A." + p + "cpCurrentMonthDate,A:visited." + p + "cpCurrentMonthDate,." + p + "cpCurrentMonthDateDisabled,." + p + "cpOtherMonthDate,." + p + "cpOtherMonthDateDisabled,." + p + "cpCurrentDate,A." + p + "cpCurrentDate,A:visited." + p + "cpCurrentDate,." + p + "cpCurrentDateDisabled,." + p + "cpTodayText,A." + p + "cpTodayText,A:visited." + p + "cpTodayText,." + p + "cpTodayTextDisabled,." + p + "cpText { color:#000000; font-family:verdana,arial,helvetica,sans-serif; font-size:8pt; }\n";
    result += "TD." + p + "cpDayColumnHeader { text-align:right; border:solid thin #C0C0C0;border-width:0 0 1 0; }\n";
    result += "." + p + "cpCurrentMonthDate, ." + p + "cpOtherMonthDate, ." + p + "cpCurrentDate  { text-align:right; text-decoration:none; }\n";
    result += "." + p + "cpCurrentMonthDateDisabled, ." + p + "cpOtherMonthDateDisabled, ." + p + "cpCurrentDateDisabled { color:#D0D0D0; text-align:right; text-decoration:line-through; }\n";
    result += "." + p + "cpTodayDateDisabled { color:#666666; text-align:right; text-decoration:line-through; }\n";
    result += "." + p + "cpOtherMonthDate,A." + p + "cpOtherMonthDate,A:visited." + p + "cpOtherMonthDate { color:#808080; }\n";
    result += "TD." + p + "cpCurrentDate { color:white; border:solid 1px #800000; }\n";
    result += "TD." + p + "cpTodayText, TD." + p + "cpTodayTextDisabled { border:solid thin #C0C0C0; border-width:1 0 0 0;}\n";
    result += "A." + p + "cpTodayText, SPAN." + p + "cpTodayTextDisabled { height:20px; }\n";
    result += "." + p + "cpTodayTextDisabled { color:#D0D0D0; }\n";
    result += "." + p + "cpBorder { border:solid 1px #dddddd; }\n";
    result += "." + p + "cpTodayDate { background-color:rgb(244, 224, 100); }\n";
    result += "</STYLE>\n";
    return result;
}
function CP_getCalendar() {
    var now = new Date();
    if (this.type == "WINDOW") {
        var windowref = "window.opener.";
    } else {
        var windowref = "";
    }
    var result = "";
    var highlightCurrentDate = true;
    if (this.type == "WINDOW") {
        result += this.getStyles() + "\n";
        result += "<CENTER><TABLE BORDER=0 BORDERWIDTH=0 CELLSPACING=0 CELLPADDING=0>\n";
    } else {
        result += '<TABLE CLASS="' + this.cssPrefix + 'cpBorder" WIDTH=167 BORDER=0 CELLSPACING=0 CELLPADDING=1>\n';
        result += "<TR><TD ALIGN=CENTER>\n";
        result += "<CENTER>\n";
    }
    if (this.displayType == "date" || this.displayType == "week-end") {
        if (this.currentDate == null) {
            this.currentDate = now;
            highlightCurrentDate = this.defaultSelectToday;
        }
        if (arguments.length > 0) {
            var month = arguments[0];
        } else {
            var month = this.currentDate.getMonth() + 1;
        }
        if (arguments.length > 1 && arguments[1] > 0 && arguments[1] - 0 == arguments[1]) {
            var year = arguments[1];
        } else {
            var year = this.currentDate.getFullYear();
        }
        var daysinmonth = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
        if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) {
            daysinmonth[2] = 29;
        }
        var current_month = new Date(year, month - 1, 1);
        var display_year = year;
        var display_month = month;
        var display_date = 1;
        var weekday = current_month.getDay();
        var offset = 0;
        offset = (weekday >= this.weekStartDay) ? weekday - this.weekStartDay: 7 - this.weekStartDay + weekday;
        if (offset > 0) {
            display_month--;
            if (display_month < 1) {
                display_month = 12;
                display_year--;
            }
            display_date = daysinmonth[display_month] - offset + 1;
        }
        var next_month = month + 1;
        var next_month_year = year;
        if (next_month > 12) {
            next_month = 1;
            next_month_year++;
        }
        var last_month = month - 1;
        var last_month_year = year;
        if (last_month < 1) {
            last_month = 12;
            last_month_year--;
        }
        var date_class;
        if (this.type != "WINDOW") {
            result += "<TABLE WIDTH=100% BORDER=0 BORDERWIDTH=0 CELLSPACING=0 CELLPADDING=3>";
        }
        result += "<TR>\n";
        var refresh = windowref + "CP_refreshCalendar";
        var refreshLink = "javascript:" + refresh;
        if (this.isShowNavigationDropdowns) {
            result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="78" COLSPAN="3"><select CLASS="' + this.cssPrefix + 'cpMonthNavigation" name="cpMonth" onChange="' + refresh + "(" + this.index + ",this.options[this.selectedIndex].value-0," + (year - 0) + ');">';
            for (var monthCounter = 1; monthCounter <= 12; monthCounter++) {
                var selected = (monthCounter == month) ? "SELECTED": "";
                result += '<option value="' + monthCounter + '" ' + selected + ">" + this.monthNames[monthCounter - 1] + "</option>";
            }
            result += "</select></TD>";
            result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="10">&nbsp;</TD>';
            result += '<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="56" COLSPAN="3"><select CLASS="' + this.cssPrefix + 'cpYearNavigation" name="cpYear" onChange="' + refresh + "(" + this.index + "," + month + ',this.options[this.selectedIndex].value-0);">';
            for (var yearCounter = year - this.yearSelectStartOffset; yearCounter <= year + this.yearSelectStartOffset; yearCounter++) {
                var selected = (yearCounter == year) ? "SELECTED": "";
                result += '<option value="' + yearCounter + '" ' + selected + ">" + yearCounter + "</option>";
            }
            result += "</select></TD>";
        } else {
            if (this.isShowYearNavigation) {
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="10"><A CLASS="' + this.cssPrefix + 'cpMonthNavigation" HREF="' + refreshLink + "(" + this.index + "," + last_month + "," + last_month_year + ');">&lt;</A></TD>';
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="58"><SPAN CLASS="' + this.cssPrefix + 'cpMonthNavigation">' + this.monthNames[month - 1] + "</SPAN></TD>";
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="10"><A CLASS="' + this.cssPrefix + 'cpMonthNavigation" HREF="' + refreshLink + "(" + this.index + "," + next_month + "," + next_month_year + ');">&gt;</A></TD>';
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="10">&nbsp;</TD>';
                result += '<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="10"><A CLASS="' + this.cssPrefix + 'cpYearNavigation" HREF="' + refreshLink + "(" + this.index + "," + month + "," + (year - 1) + ');">&lt;</A></TD>';
                if (this.isShowYearNavigationInput) {
                    result += '<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="36"><INPUT NAME="cpYear" CLASS="' + this.cssPrefix + 'cpYearNavigation" SIZE="4" MAXLENGTH="4" VALUE="' + year + '" onBlur="' + refresh + "(" + this.index + "," + month + ',this.value-0);"></TD>';
                } else {
                    result += '<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="36"><SPAN CLASS="' + this.cssPrefix + 'cpYearNavigation">' + year + "</SPAN></TD>";
                }
                result += '<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="10"><A CLASS="' + this.cssPrefix + 'cpYearNavigation" HREF="' + refreshLink + "(" + this.index + "," + month + "," + (year + 1) + ');">&gt;</A></TD>';
            } else {
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="22"><A CLASS="' + this.cssPrefix + 'cpMonthNavigation" HREF="' + refreshLink + "(" + this.index + "," + last_month + "," + last_month_year + ');">&lt;&lt;</A></TD>\n';
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="100"><SPAN CLASS="' + this.cssPrefix + 'cpMonthNavigation">' + this.monthNames[month - 1] + "&nbsp;" + year + "</SPAN></TD>\n";
                result += '<TD CLASS="' + this.cssPrefix + 'cpMonthNavigation" WIDTH="22"><A CLASS="' + this.cssPrefix + 'cpMonthNavigation" HREF="' + refreshLink + "(" + this.index + "," + next_month + "," + next_month_year + ');">&gt;&gt;</A></TD>\n';
            }
        }
        result += "</TR></TABLE>\n";
        result += "<TABLE WIDTH=120 BORDER=0 CELLSPACING=0 CELLPADDING=2 ALIGN=CENTER>\n";
        result += "<TR>\n";
        for (var j = 0; j < 7; j++) {
            result += '<TD CLASS="' + this.cssPrefix + 'cpDayColumnHeader" WIDTH="14%"><SPAN CLASS="' + this.cssPrefix + 'cpDayColumnHeader">' + this.dayHeaders[(this.weekStartDay + j) % 7] + "</TD>\n";
        }
        result += "</TR>\n";
        for (var row = 1; row <= 6; row++) {
            result += "<TR>\n";
            for (var col = 1; col <= 7; col++) {
                var disabled = false;
                if (this.disabledDatesExpression != "") {
                    var ds = "" + display_year + LZ(display_month) + LZ(display_date);
                    eval("disabled=(" + this.disabledDatesExpression + ")");
                }
                var dateClass = "";
                if ((highlightCurrentDate) && (display_month == this.currentDate.getMonth() + 1) && (display_date == this.currentDate.getDate()) && (display_year == this.currentDate.getFullYear())) {
                    dateClass = this.cssPrefix + "cpCurrentDate";
                } else {
                    if (display_month == month) {
                        dateClass = this.cssPrefix + "cpCurrentMonthDate";
                    } else {
                        dateClass = this.cssPrefix + "cpOtherMonthDate";
                    }
                }
                if ((display_month == now.getMonth() + 1) && (display_date == now.getDate()) && (display_year == now.getFullYear())) {
                    dateClass += " " + this.cssPrefix + "cpTodayDate";
                }
                if (disabled || this.disabledWeekDays[col - 1]) {
                    result += '	<TD CLASS="' + dateClass + '"><SPAN CLASS="' + dateClass + 'Disabled">' + display_date + "</SPAN></TD>\n";
                } else {
                    var selected_date = display_date;
                    var selected_month = display_month;
                    var selected_year = display_year;
                    if (this.displayType == "week-end") {
                        var d = new Date(selected_year, selected_month - 1, selected_date, 0, 0, 0, 0);
                        d.setDate(d.getDate() + (7 - col));
                        selected_year = d.getYear();
                        if (selected_year < 1000) {
                            selected_year += 1900;
                        }
                        selected_month = d.getMonth() + 1;
                        selected_date = d.getDate();
                    }
                    result += '	<TD CLASS="' + dateClass + '"><A HREF="javascript:' + windowref + this.returnFunction + "(" + selected_year + "," + selected_month + "," + selected_date + ");" + windowref + "CP_hideCalendar('" + this.index + '\');" CLASS="' + dateClass + '">' + display_date + "</A></TD>\n";
                }
                display_date++;
                if (display_date > daysinmonth[display_month]) {
                    display_date = 1;
                    display_month++;
                }
                if (display_month > 12) {
                    display_month = 1;
                    display_year++;
                }
            }
            result += "</TR>";
        }
        var current_weekday = now.getDay() - this.weekStartDay;
        if (current_weekday < 0) {
            current_weekday += 7;
        }
        if (this.showTodayLink) {
            result += "<TR>\n";
            result += '	<TD COLSPAN=7 ALIGN=CENTER CLASS="' + this.cssPrefix + 'cpTodayText">\n';
            if (this.disabledDatesExpression != "") {
                var ds = "" + now.getFullYear() + LZ(now.getMonth() + 1) + LZ(now.getDate());
                eval("disabled=(" + this.disabledDatesExpression + ")");
            }
            if (disabled || this.disabledWeekDays[current_weekday + 1]) {
                result += '		<SPAN CLASS="' + this.cssPrefix + 'cpTodayTextDisabled">' + this.todayText + "</SPAN>\n";
            } else {
                result += '		<A CLASS="' + this.cssPrefix + 'cpTodayText" HREF="javascript:' + windowref + this.returnFunction + "('" + now.getFullYear() + "','" + (now.getMonth() + 1) + "','" + now.getDate() + "');" + windowref + "CP_hideCalendar('" + this.index + "');\">" + this.todayText + "</A>\n";
            }
            result += "		<BR>\n";
            result += "	</TD></TR>";
        }
        result += "</TABLE></CENTER></TD></TR></TABLE>\n";
    }
    if (this.displayType == "month" || this.displayType == "quarter" || this.displayType == "year") {
        if (arguments.length > 0) {
            var year = arguments[0];
        } else {
            if (this.displayType == "year") {
                var year = now.getFullYear() - this.yearSelectStartOffset;
            } else {
                var year = now.getFullYear();
            }
        }
        if (this.displayType != "year" && this.isShowYearNavigation) {
            result += "<TABLE WIDTH=144 BORDER=0 BORDERWIDTH=0 CELLSPACING=0 CELLPADDING=0>";
            result += "<TR>\n";
            result += '	<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="22"><A CLASS="' + this.cssPrefix + 'cpYearNavigation" HREF="javascript:' + windowref + "CP_refreshCalendar(" + this.index + "," + (year - 1) + ');">&lt;&lt;</A></TD>\n';
            result += '	<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="100">' + year + "</TD>\n";
            result += '	<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="22"><A CLASS="' + this.cssPrefix + 'cpYearNavigation" HREF="javascript:' + windowref + "CP_refreshCalendar(" + this.index + "," + (year + 1) + ');">&gt;&gt;</A></TD>\n';
            result += "</TR></TABLE>\n";
        }
    }
    if (this.displayType == "month") {
        result += "<TABLE WIDTH=120 BORDER=0 CELLSPACING=1 CELLPADDING=0 ALIGN=CENTER>\n";
        for (var i = 0; i < 4; i++) {
            result += "<TR>";
            for (var j = 0; j < 3; j++) {
                var monthindex = ((i * 3) + j);
                result += '<TD WIDTH=33% ALIGN=CENTER><A CLASS="' + this.cssPrefix + 'cpText" HREF="javascript:' + windowref + this.returnMonthFunction + "(" + year + "," + (monthindex + 1) + ");" + windowref + "CP_hideCalendar('" + this.index + '\');" CLASS="' + date_class + '">' + this.monthAbbreviations[monthindex] + "</A></TD>";
            }
            result += "</TR>";
        }
        result += "</TABLE></CENTER></TD></TR></TABLE>\n";
    }
    if (this.displayType == "quarter") {
        result += "<BR><TABLE WIDTH=120 BORDER=1 CELLSPACING=0 CELLPADDING=0 ALIGN=CENTER>\n";
        for (var i = 0; i < 2; i++) {
            result += "<TR>";
            for (var j = 0; j < 2; j++) {
                var quarter = ((i * 2) + j + 1);
                result += '<TD WIDTH=50% ALIGN=CENTER><BR><A CLASS="' + this.cssPrefix + 'cpText" HREF="javascript:' + windowref + this.returnQuarterFunction + "(" + year + "," + quarter + ");" + windowref + "CP_hideCalendar('" + this.index + '\');" CLASS="' + date_class + '">Q' + quarter + "</A><BR><BR></TD>";
            }
            result += "</TR>";
        }
        result += "</TABLE></CENTER></TD></TR></TABLE>\n";
    }
    if (this.displayType == "year") {
        var yearColumnSize = 4;
        result += "<TABLE WIDTH=144 BORDER=0 BORDERWIDTH=0 CELLSPACING=0 CELLPADDING=0>";
        result += "<TR>\n";
        result += '	<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="50%"><A CLASS="' + this.cssPrefix + 'cpYearNavigation" HREF="javascript:' + windowref + "CP_refreshCalendar(" + this.index + "," + (year - (yearColumnSize * 2)) + ');">&lt;&lt;</A></TD>\n';
        result += '	<TD CLASS="' + this.cssPrefix + 'cpYearNavigation" WIDTH="50%"><A CLASS="' + this.cssPrefix + 'cpYearNavigation" HREF="javascript:' + windowref + "CP_refreshCalendar(" + this.index + "," + (year + (yearColumnSize * 2)) + ');">&gt;&gt;</A></TD>\n';
        result += "</TR></TABLE>\n";
        result += "<TABLE WIDTH=120 BORDER=0 CELLSPACING=1 CELLPADDING=0 ALIGN=CENTER>\n";
        for (var i = 0; i < yearColumnSize; i++) {
            for (var j = 0; j < 2; j++) {
                var currentyear = year + (j * yearColumnSize) + i;
                result += '<TD WIDTH=50% ALIGN=CENTER><A CLASS="' + this.cssPrefix + 'cpText" HREF="javascript:' + windowref + this.returnYearFunction + "(" + currentyear + ");" + windowref + "CP_hideCalendar('" + this.index + '\');" CLASS="' + date_class + '">' + currentyear + "</A></TD>";
            }
            result += "</TR>";
        }
        result += "</TABLE></CENTER></TD></TR></TABLE>\n";
    }
    return result;
}
var MONTH_NAMES = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
var DAY_NAMES = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
function LZ(x) {
    return (x < 0 || x > 9 ? "": "0") + x;
}
function isDate(val, format) {
    var date = getDateFromFormat(val, format);
    if (date == 0) {
        return false;
    }
    return true;
}
function compareDates(date1, dateformat1, date2, dateformat2) {
    var d1 = getDateFromFormat(date1, dateformat1);
    var d2 = getDateFromFormat(date2, dateformat2);
    if (d1 == 0 || d2 == 0) {
        return - 1;
    } else {
        if (d1 > d2) {
            return 1;
        }
    }
    return 0;
}
function formatDate(date, format) {
    format = format + "";
    var result = "";
    var i_format = 0;
    var c = "";
    var token = "";
    var y = date.getYear() + "";
    var M = date.getMonth() + 1;
    var d = date.getDate();
    var E = date.getDay();
    var H = date.getHours();
    var m = date.getMinutes();
    var s = date.getSeconds();
    var yyyy, yy, MMM, MM, dd, hh, h, mm, ss, ampm, HH, H, KK, K, kk, k;
    var value = new Object();
    if (y.length < 4) {
        y = "" + (y - 0 + 1900);
    }
    value["y"] = "" + y;
    value["yyyy"] = y;
    value["yy"] = y.substring(2, 4);
    value["M"] = M;
    value["MM"] = LZ(M);
    value["MMM"] = MONTH_NAMES[M - 1];
    value["NNN"] = MONTH_NAMES[M + 11];
    value["d"] = d;
    value["dd"] = LZ(d);
    value["E"] = DAY_NAMES[E + 7];
    value["EE"] = DAY_NAMES[E];
    value["H"] = H;
    value["HH"] = LZ(H);
    if (H == 0) {
        value["h"] = 12;
    } else {
        if (H > 12) {
            value["h"] = H - 12;
        } else {
            value["h"] = H;
        }
    }
    value["hh"] = LZ(value["h"]);
    if (H > 11) {
        value["K"] = H - 12;
    } else {
        value["K"] = H;
    }
    value["k"] = H + 1;
    value["KK"] = LZ(value["K"]);
    value["kk"] = LZ(value["k"]);
    if (H > 11) {
        value["a"] = "PM";
    } else {
        value["a"] = "AM";
    }
    value["m"] = m;
    value["mm"] = LZ(m);
    value["s"] = s;
    value["ss"] = LZ(s);
    while (i_format < format.length) {
        c = format.charAt(i_format);
        token = "";
        while ((format.charAt(i_format) == c) && (i_format < format.length)) {
            token += format.charAt(i_format++);
        }
        if (value[token] != null) {
            result = result + value[token];
        } else {
            result = result + token;
        }
    }
    return result;
}
function _isInteger(val) {
    var digits = "1234567890";
    for (var i = 0; i < val.length; i++) {
        if (digits.indexOf(val.charAt(i)) == -1) {
            return false;
        }
    }
    return true;
}
function _getInt(str, i, minlength, maxlength) {
    for (var x = maxlength; x >= minlength; x--) {
        var token = str.substring(i, i + x);
        if (token.length < minlength) {
            return null;
        }
        if (_isInteger(token)) {
            return token;
        }
    }
    return null;
}
function getDateFromFormat(val, format) {
    val = val + "";
    format = format + "";
    var i_val = 0;
    var i_format = 0;
    var c = "";
    var token = "";
    var token2 = "";
    var x, y;
    var now = new Date();
    var year = now.getYear();
    var month = now.getMonth() + 1;
    var date = 1;
    var hh = now.getHours();
    var mm = now.getMinutes();
    var ss = now.getSeconds();
    var ampm = "";
    while (i_format < format.length) {
        c = format.charAt(i_format);
        token = "";
        while ((format.charAt(i_format) == c) && (i_format < format.length)) {
            token += format.charAt(i_format++);
        }
        if (token == "yyyy" || token == "yy" || token == "y") {
            if (token == "yyyy") {
                x = 4;
                y = 4;
            }
            if (token == "yy") {
                x = 2;
                y = 2;
            }
            if (token == "y") {
                x = 2;
                y = 4;
            }
            year = _getInt(val, i_val, x, y);
            if (year == null) {
                return 0;
            }
            i_val += year.length;
            if (year.length == 2) {
                if (year > 70) {
                    year = 1900 + (year - 0);
                } else {
                    year = 2000 + (year - 0);
                }
            }
        } else {
            if (token == "MMM" || token == "NNN") {
                month = 0;
                for (var i = 0; i < MONTH_NAMES.length; i++) {
                    var month_name = MONTH_NAMES[i];
                    if (val.substring(i_val, i_val + month_name.length).toLowerCase() == month_name.toLowerCase()) {
                        if (token == "MMM" || (token == "NNN" && i > 11)) {
                            month = i + 1;
                            if (month > 12) {
                                month -= 12;
                            }
                            i_val += month_name.length;
                            break;
                        }
                    }
                }
                if ((month < 1) || (month > 12)) {
                    return 0;
                }
            } else {
                if (token == "EE" || token == "E") {
                    for (var i = 0; i < DAY_NAMES.length; i++) {
                        var day_name = DAY_NAMES[i];
                        if (val.substring(i_val, i_val + day_name.length).toLowerCase() == day_name.toLowerCase()) {
                            i_val += day_name.length;
                            break;
                        }
                    }
                } else {
                    if (token == "MM" || token == "M") {
                        month = _getInt(val, i_val, token.length, 2);
                        if (month == null || (month < 1) || (month > 12)) {
                            return 0;
                        }
                        i_val += month.length;
                    } else {
                        if (token == "dd" || token == "d") {
                            date = _getInt(val, i_val, token.length, 2);
                            if (date == null || (date < 1) || (date > 31)) {
                                return 0;
                            }
                            i_val += date.length;
                        } else {
                            if (token == "hh" || token == "h") {
                                hh = _getInt(val, i_val, token.length, 2);
                                if (hh == null || (hh < 1) || (hh > 12)) {
                                    return 0;
                                }
                                i_val += hh.length;
                            } else {
                                if (token == "HH" || token == "H") {
                                    hh = _getInt(val, i_val, token.length, 2);
                                    if (hh == null || (hh < 0) || (hh > 23)) {
                                        return 0;
                                    }
                                    i_val += hh.length;
                                } else {
                                    if (token == "KK" || token == "K") {
                                        hh = _getInt(val, i_val, token.length, 2);
                                        if (hh == null || (hh < 0) || (hh > 11)) {
                                            return 0;
                                        }
                                        i_val += hh.length;
                                    } else {
                                        if (token == "kk" || token == "k") {
                                            hh = _getInt(val, i_val, token.length, 2);
                                            if (hh == null || (hh < 1) || (hh > 24)) {
                                                return 0;
                                            }
                                            i_val += hh.length;
                                            hh--;
                                        } else {
                                            if (token == "mm" || token == "m") {
                                                mm = _getInt(val, i_val, token.length, 2);
                                                if (mm == null || (mm < 0) || (mm > 59)) {
                                                    return 0;
                                                }
                                                i_val += mm.length;
                                            } else {
                                                if (token == "ss" || token == "s") {
                                                    ss = _getInt(val, i_val, token.length, 2);
                                                    if (ss == null || (ss < 0) || (ss > 59)) {
                                                        return 0;
                                                    }
                                                    i_val += ss.length;
                                                } else {
                                                    if (token == "a") {
                                                        if (val.substring(i_val, i_val + 2).toLowerCase() == "am") {
                                                            ampm = "AM";
                                                        } else {
                                                            if (val.substring(i_val, i_val + 2).toLowerCase() == "pm") {
                                                                ampm = "PM";
                                                            } else {
                                                                return 0;
                                                            }
                                                        }
                                                        i_val += 2;
                                                    } else {
                                                        if (val.substring(i_val, i_val + token.length) != token) {
                                                            return 0;
                                                        } else {
                                                            i_val += token.length;
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if (i_val != val.length) {
        return 0;
    }
    if (month == 2) {
        if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) {
            if (date > 29) {
                return 0;
            }
        } else {
            if (date > 28) {
                return 0;
            }
        }
    }
    if ((month == 4) || (month == 6) || (month == 9) || (month == 11)) {
        if (date > 30) {
            return 0;
        }
    }
    if (hh < 12 && ampm == "PM") {
        hh = hh - 0 + 12;
    } else {
        if (hh > 11 && ampm == "AM") {
            hh -= 12;
        }
    }
    var newdate = new Date(year, month - 1, date, hh, mm, ss);
    return newdate.getTime();
}
function parseDate(val) {
    var preferEuro = (arguments.length == 2) ? arguments[1] : false;
    var format = getFormatFromDate(val, preferEuro);
    if (format) {
        d = getDateFromFormat(val, format);
        if (d != 0) {
            return new Date(d);
        }
    }
    return null;
}
function getFormatFromDate(dateString) {
    var preferEuro = (arguments.length == 2) ? arguments[1] : false;
    generalFormats = new Array("y-M-d", "MMM d, y", "MMM d,y", "y-MMM-d", "d-MMM-y", "d MMM y", "MMM d");
    monthFirst = new Array("M/d/y", "M-d-y", "M.d.y", "MMM-d", "M/d", "M-d");
    dateFirst = new Array("d/M/y", "d-M-y", "d.M.y", "d-MMM", "d/M", "d-M");
    checkList = new Array("generalFormats", preferEuro ? "dateFirst": "monthFirst", preferEuro ? "monthFirst": "dateFirst");
    var d = null;
    for (var i = 0; i < checkList.length; i++) {
        var l = window[checkList[i]];
        for (var j = 0; j < l.length; j++) {
            d = getDateFromFormat(dateString, l[j]);
            if (d != 0) {
                return l[j];
            }
        }
    }
}
amznJQ.available("popover",
function() {
    var initPopover = function(contextualWidgetId) {
        var associatedFeature = contextualWidgetId,
        contextualPopupOptions = {
            showOnHover: true,
            width: 280,
            hoverShowDelay: 300,
            hoverHideDelay: 200,
            locationOffset: [15, 0],
            showCloseButton: false,
            attached: true,
            align: "middle",
            location: "auto",
            localContent: "#" + contextualWidgetId + "_Div_Id",
            ajaxTimeout: 5000,
            ajaxErrorContent: '<div class="popover-title">Sorry we encountered a problem.</div>',
            onHide: function() {
                SCS.SCITS.appendAndSendMetrics({
                    clientProgram: "Payment Summary",
                    associatedFeature: associatedFeature
                });
            }
        };
        jQuery("#" + contextualWidgetId).amazonPopoverTrigger(contextualPopupOptions);
    },
    contextual_help_string_ids = ["SellerPayments_UI_ContextualHelp_Orders", "SellerPayments_UI_ContextualHelp_Orders_ProductCharges", "SellerPayments_UI_ContextualHelp_Orders_PromoRebates", "SellerPayments_UI_ContextualHelp_Orders_Cost_of_Points", "SellerPayments_UI_ContextualHelp_Orders_AmazonFees", "SellerPayments_UI_ContextualHelp_Orders_Other", "SellerPayments_UI_ContextualHelp_Refunds", "SellerPayments_UI_ContextualHelp_Refunds_ProductCharges", "SellerPayments_UI_ContextualHelp_Refunds_PromoRebates", "SellerPayments_UI_ContextualHelp_Refunds_Cost_of_Points", "SellerPayments_UI_ContextualHelp_Refunds_AmazonFees", "SellerPayments_UI_ContextualHelp_Refunds_PerformanceBondRefund", "SellerPayments_UI_ContextualHelp_Refunds_Other", "SellerPayments_UI_ContextualHelp_ServiceFeeRefund", "SellerPayments_UI_ContextualHelp_ServiceFeeRefunds_ReferralFee", "SellerPayments_UI_ContextualHelp_ServiceFeeRefunds_TaxCollection", "SellerPayments_UI_ContextualHelp_ServiceFeeRefunds_SellerOrderCredit", "SellerPayments_UI_ContextualHelp_ServiceFeeRefunds_GiftWrap", "SellerPayments_UI_ContextualHelp_ServiceFeeRefunds_subscriptionFee", "SellerPayments_UI_ContextualHelp_OtherTransactions", "SellerPayments_UI_ContextualHelp_OtherTransactions_AmazonFees", "SellerPayments_UI_ContextualHelp_OtherTransactions_Other", "SellerPayments_UI_ContextualHelp_ShippingService", "SellerPayments_UI_ContextualHelp_ShippingService_Charges", "SellerPayments_UI_ContextualHelp_ShippingService_Refunds", "SellerPayments_UI_ContextualHelp_ShippingService_Chargebacks", "SellerPayments_UI_ContextualHelp_ShippingService_AmazonFees", "SellerPayments_UI_ContextualHelp_ShippingService_Other", "SellerPayments_UI_ContextualHelp_Balance", "SellerPayments_UI_ContextualHelp_ClosingBalance", "SellerPayments_UI_ContextualHelp_ClosingBalance_Payment", "SellerPayments_UI_ContextualHelp_ClosingBalance_ReserveAmount", "SellerPayments_UI_ContextualHelp_ClosingBalance_CurrentPaymentAmount", "SellerPayments_UI_ContextualHelp_ClosingBalance_NetProceeds", "SellerPayments_UI_ContextualHelp_ReserveAmount", "SellerPayments_UI_ContextualHelp_CurrentSettlement", "SellerPayments_UI_ContextualHelp_CurrentAvailableBalance", "SellerPayments_UI_ContextualHelp_SettlementDate", "SellerPayments_UI_ContextualHelp_FindATransaction", "SellerPayments_UI_ContextualHelp_Amazon_Capital_Services", "SellerPayments_UI_ContextualHelp_Pending_Amazon_Capital_Services_Payments", "SellerPayments_UI_ContextualHelp_BeginningBalance", "SellerPayments_UI_ContextualHelp_BeginningBalance_Carryover", "SellerPayments_UI_ContextualHelp_BeginningBalance_Debt", "SellerPayments_UI_ContextualHelp_DebtRecovery", "SellerPayments_UI_ContextualHelp_DebtRecovery_DebtPayment", "SellerPayments_UI_ContextualHelp_DebtRecovery_DebtForgiven", "sellerpayments_myp_lastStatementUnavailableBalance_contextualhelp", "sellerpayments_myp_carryoverDebt_contextualhelp", "sellerpayments_myp_carryoverFailedTransfer_contextualhelp", "sellerpayments_myp_closing_balance_contextualhelp", "sellerpayments_myp_totalBalance_contextualhelp", "sellerpayments_myp_lastStatementUnavailableBalance_contextualhelp", "sellerpayments_myp_transferAmount_contextualhelp", "sellerpayments_myp_shipping_gift_wrap_credits_contextualhelp", "sellerpayments_myp_shipping_label_charges_contextual_help", "sellerpayments_myp_miscellaneousAdjustments_contextualhelp", "sellerpayments_myp_fbaInventoryFees_contextualhelp", "sellerpayments_myp_subscriptionFees_contextualhelp", "sellerpayments_myp_shipping_gift_wrap_credits_contextualhelp", "SellerPayments_UI_ContextualHelp_ChargebackRefunds", "SellerPayments_UI_ContextualHelp_ChargebackRefunds_ProductCharges", "SellerPayments_UI_ContextualHelp_ChargebackRefunds_AmazonFees", "SellerPayments_UI_ContextualHelp_ChargebackRefunds_Other", "SellerPayments_UI_ContextualHelp_GuaranteeClaimRefunds", "SellerPayments_UI_ContextualHelp_GuaranteeClaimRefunds_ProductCharges", "SellerPayments_UI_ContextualHelp_GuaranteeClaimRefunds_AmazonFees", "SellerPayments_UI_ContextualHelp_GuaranteeClaimRefunds_Other", "SellerPayments_UI_ContextualHelp_ServiceFee", "SellerPayments_UI_ContextualHelp_ServiceFee_AmazonFees", "SellerPayments_UI_ContextualHelp_ServiceFee_GiftWrap", "SellerPayments_UI_ContextualHelp_ServiceFee_Other", "SellerPayments_UI_ContextualHelp_ServiceFee_ReferralFee", "SellerPayments_UI_ContextualHelp_ServiceFee_SellerOrderCredit", "SellerPayments_UI_ContextualHelp_ServiceFee_TaxCollection", "SellerPayments_UI_ContextualHelp_ServiceFee_AdvertisingFee", "SellerPayments_UI_ContextualHelp_ServiceFee_AdvertisingFeeRefund", "SellerPayments_UI_ContextualHelp_Orders_DirectPayment", "SellerPayments_UI_ContextualHelp_Refunds_DirectPayment", "SellerPayments_UI_TransactionView_ReportSizeLimit_ContextualHelp", "SellerPayments_UI_SettlementSummary_TraceId_ContextualHelp", "SellerPayments_UI_ContextualHelp_Orders_Provider_Amount", "SellerPayments_UI_ContextualHelp_Refunds_Provider_Amount", "SellerPayments_UI_ContextualHelp_GuaranteeClaimRefunds_Provider_Amount", "SellerPayments_UI_ContextualHelp_ChargebackRefunds_Provider_Amount", ];
    for (var index = 0; index < contextual_help_string_ids.length; index++) {
        initPopover(contextual_help_string_ids[index]);
    }
}); (function($) {
    var testElem = document.createElement("input"),
    supported = ("placeholder" in testElem);
    if (!supported) {
        $(function() {
            $("input[placeholder]").live("focus",
            function() {
                var $this = $(this);
                if ($this.val() === $this.attr("placeholder")) {
                    $this.val("").removeClass("grey");
                }
            }).live("blur",
            function() {
                var $this = $(this),
                val = $this.val(),
                placeholder = $this.attr("placeholder");
                if (val === "" || val === placeholder) {
                    $this.val(placeholder).addClass("grey");
                } else {
                    $this.removeClass("grey");
                }
            }).blur();
            $("form").live("submit",
            function() {
                $(this).find("input[placeholder]").each(function() {
                    var $this = $(this);
                    if ($this.val() === $this.attr("placeholder")) {
                        $this.val("");
                    }
                });
            });
        });
    }
})(jQuery); (function($, undefined) {
    $(".repaydebtspopovertrigger").amazonPopoverTrigger({
        localContent: "#repayBalancesPopover",
        width: 750,
        height: 750,
        draggable: true,
        closeEventExclude: "CLICK_OUTSIDE",
        title: RUI.strings.repayTitle,
        onShow: scFixPopoverStacking
    });
    $(".repayBalancesPopover select, .repayBalancesPopover input[type=text]").each(function() {
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
    $generateButton = $('button[name="Submit payment"]');
    $generateButton.click(function() {
        submitPaymentAction();
    });
    $cancelButton = $("a[name=Cancel]");
    $cancelButton.click(function() {
        $('button[name="Submit payment"]').show();
    });
    function submitPaymentAction() {
        var queryParams, $paymentAmount = $("input[name=debtsPaymentAmount]:checked").attr("id").split("debtsPaymentRadio")[1];
        var $paymentInstrumentId = $("#paymentInstruments").val();
        var $otherAmountValue = $("#otherAmountValue").val();
        if ($paymentAmount === "OtherAmount") {
            var regex = /^\d+(\.{0,1}\d{0,2})$/;
            if (!regex.test($otherAmountValue)) {
                amountError(RUI.strings.enterDollarAmount);
                return;
            }
            if (validateEmptyOrUndefined($otherAmountValue)) {
                amountError(RUI.strings.noValue);
                return;
            }
        }
        $("button[name=Cancel]").hide();
        $('button[name="Submit payment"]').hide();
        var funct = function() {
            jQuery.post("/gp/payments-account/submit-payment.html", {
                paymentInstrumentId: $paymentInstrumentId,
                amount: $otherAmountValue
            },
            function(data) {
                window.location.reload();
            });
        };
        alertPopover(RUI.strings.submissionRegistered, funct);
    }
    function validateEmptyOrUndefined(stringContent) {
        if (stringContent === "" || stringContent == undefined) {
            return true;
        }
        return false;
    }
    function amountError(error) {
        alertPopover(error, null);
    }
    function alertPopover(message, funct) {
        var popoverParams = {
            width: 350,
            position: "over",
            modal: true,
            closeEventExclude: ["CLICK_OUTSIDE"],
            literalContent: "<div style='text-align=center;'><p>" + message + "</p><p align='center'><button type='button' onclick='#close' class='ap_custom_close'>OK</button></p></div>"
        };
        if (null != funct) {
            popoverParams["onHide"] = funct;
        }
        jQuery.AmazonPopover.displayPopover(popoverParams);
    }
})(jQuery);
amznJQ.declareAvailable("repayments-popup"); (function($, undefined) {
    $(".mypportalrepaybutton").click(function() {
        window.location = ("/payments/repayment/details");
    });
})(jQuery);
amznJQ.declareAvailable("repayments");
amznJQ.available("popover",
function() {
    jQuery(".showFuturePaymentsPopOver").amazonPopoverTrigger({
        showOnHover: false,
        onFilled: function(popover, settings) {
            jQuery(popover).find("#sc_footer_container").detach();
        },
        destination: $(".showFuturePaymentsPopOver").attr("href"),
        title: "&nbsp",
        showCloseButton: true,
        location: "centered",
        draggable: true,
        ajaxErrorContent: '<div style="color:red" popoverTitle="Error">' + $(".showFuturePaymentsPopOver").attr("error") + "</div>",
        ajaxTimeout: 6000,
        width: 400
    });
});
amznJQ.onReady("JQuery",
function() {
    function getReserveBalanceInfoAjax(url, arguments, callback) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4) {
                callback(xmlhttp.readyState, xmlhttp.status, xmlhttp.responseText);
            }
        };
        if (arguments != null && arguments.length > 0) {
            url = url + "?";
            for (var i = 0; i < arguments.length; i++) {
                if (i == 0) {
                    url = url + arguments[i];
                } else {
                    url = url + "&" + arguments[i];
                }
            }
        }
        xmlhttp.open("GET", url, false);
        xmlhttp.send();
    }
    function cutOutRelevantData(input, start, end) {
        var sPos = input.indexOf(start) + start.length;
        var ePos = input.indexOf(end);
        if (sPos != -1 && ePos != -1) {
            return input.substring(sPos, ePos);
        }
        return input;
    }
    function parseInputLines(input, delimiter) {
        var lines = input.split("\n");
        for (i in lines) {
            var data = lines[i].split(delimiter);
            if (data[0] != null && data[1] != null) {
                addPaymentLine(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], i);
            }
        }
    }
    function addPaymentLine(text, amount, reason, helpNodeId, enMarketplaceId, finacialGroupId, doNotMakeUnavailableBalanceLinkClickable, constructUBUrlFlag, index) {
        var helpText = "<strong>" + reason + "</strong>";
        var helpId = "reserveDetail_" + index + "_contextual_help";
        var helpDivId = helpId + "_Div_Id";
        var unavailableBalanceUrl;
        var htmlForAmount = "";
        if (constructUBUrlFlag == "True" && 1 != doNotMakeUnavailableBalanceLinkClickable) {
            unavailableBalanceUrl = "<a href='/payments/reports/unavailable-balance/details?groupId=" + finacialGroupId + "&enMarketplaceId=" + enMarketplaceId + "'>" + amount + "</a>";
            htmlForAmount = '<span class="pNegativeHelpAnchorUndotted" id=' + helpId + ">" + unavailableBalanceUrl + '</span><div style="display:none" id=' + helpDivId + ">" + helpText + "</div>";
        } else {
            unavailableBalanceUrl = amount;
            if (200136810 != helpNodeId) {
                htmlForAmount = '<span class="pNegativeHelpAnchor" id=' + helpId + ">" + unavailableBalanceUrl + '</span><div style="display:none" id=' + helpDivId + ">" + helpText + "</div>";
            } else {
                htmlForAmount = '<span class="negative" id=' + helpId + ">" + unavailableBalanceUrl + '</span><div style="display:none" id=' + helpDivId + ">" + helpText + "</div>";
            }
        }
        var htmlToInsert = '<div class="pDetailLine"><div class="pDetailLineValue">' + htmlForAmount + '</div><div class="pDetailLineKey">' + text + "</div>";
        $("#reservedBalanceSlidingDrawerInnerDiv").children(".pDetailBlock").children(".pDetailBreakdown").append(htmlToInsert);
        if (constructUBUrlFlag == "False") {
            loadHelp(helpNodeId, helpDivId);
            var initPopover;
            amznJQ.available("popover",
            function() {
                initPopover = function(contextualWidgetId) {
                    var associatedFeature = contextualWidgetId,
                    contextualPopupOptions = {
                        showOnHover: true,
                        width: 280,
                        hoverShowDelay: 300,
                        hoverHideDelay: 200,
                        locationOffset: [15, 0],
                        showCloseButton: false,
                        attached: true,
                        align: "middle",
                        location: "auto",
                        localContent: "#" + contextualWidgetId + "_Div_Id",
                        ajaxTimeout: 5000,
                        ajaxErrorContent: '<div class="popover-title">Sorry we encountered a problem.</div>',
                        onHide: function() {
                            SCS.SCITS.appendAndSendMetrics({
                                clientProgram: "PaymentSummary",
                                associatedFeature: associatedFeature
                            });
                        }
                    };
                    jQuery("#" + contextualWidgetId).amazonPopoverTrigger(contextualPopupOptions);
                };
            });
            if (200136810 != helpNodeId) {
                initPopover(helpId);
            }
        }
    }
    function loadHelp(helpNodeId, helpDivId) {
        var url = "/gp/help/help-popup.html?itemID=" + helpNodeId;
        loadHelpAjax(url, [],
        function(state, status, result) {
            if (state == 4 && status == 200) {
                var sPos = result.indexOf("<div style=");
                if ( - 1 != sPos) {
                    var text = "";
                    var ePos = result.indexOf("</div>", sPos);
                    text = result.substring(sPos, ePos);
                    var tInit = result.indexOf('s.prop4="');
                    tInit += 9;
                    var title = result.substring(tInit, result.indexOf('";', tInit));
                    title = title.replace(/\w\S*/g,
                    function(txt) {
                        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                    });
                    title = "<strong>" + title + "</strong>";
                    var html = "";
                    sPos = text.indexOf("</p>");
                    sPos += 4;
                    text = text.substring(sPos);
                    html = title + "<p>" + text + "</p>";
                    $("#" + helpDivId).html(html);
                }
            }
        });
    }
    function loadHelpAjax(url, arguments, callback) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4) {
                callback(xmlhttp.readyState, xmlhttp.status, xmlhttp.responseText);
            }
        };
        xmlhttp.open("GET", url, false);
        xmlhttp.send();
    }
    var sURL = "get-reserved-balance-data.html";
    var settlementGroupId = $("#drawerSettlementId").val();
    var financialEventGroupId = $("form[name='change_settlement'] [name='groupId']").val();
    if (undefined == settlementGroupId && undefined == financialEventGroupId) {
        return;
    }
    var params = new Array();
    params[0] = "settlementGroupId=" + settlementGroupId;
    params[1] = "financialEventGroupId=" + financialEventGroupId;
    getReserveBalanceInfoAjax(sURL, params,
    function(state, status, text) {
        if (state == 4 && status == 200) {
            a = cutOutRelevantData(text, "<start>", "<end>");
            parseInputLines(a, "<sc>");
        }
    });
    $("#reservedBalanceSlidingDrawerOpener").click(function(ev) {
        var openingDelayInMS = 200;
        $("#reservedBalanceSlidingDrawer").slideToggle(openingDelayInMS);
        $(this).toggleClass("active");
        ev.preventDefault();
        return false;
    });
});

