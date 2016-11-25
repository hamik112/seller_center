/*

 This software is used under the MIT license.
 CLDR JavaScript Library v0.4.4
 http://jquery.com/

 Copyright 2013 Rafael Xavier de Souza
 Released under the MIT license
 http://jquery.org/license

 Date: 2016-01-18T12:25Z

 This software is used under the MIT license.
 CLDR JavaScript Library v0.4.4
 http://jquery.com/

 Copyright 2013 Rafael Xavier de Souza
 Released under the MIT license
 http://jquery.org/license

 Date: 2016-01-18T12:25Z

 This software is used under the MIT license.
 CLDR JavaScript Library v0.4.4
 http://jquery.com/

 Copyright 2013 Rafael Xavier de Souza
 Released under the MIT license
 http://jquery.org/license

 Date: 2016-01-18T12:25Z

 This software is used under the MIT license.
 CLDR JavaScript Library v0.4.4
 http://jquery.com/

 Copyright 2013 Rafael Xavier de Souza
 Released under the MIT license
 http://jquery.org/license

 Date: 2016-01-18T12:25Z
*/
(function(k){var r=window.AmazonUIPageJS||window.P,u=r._namespace||r.attributeErrors,d=u?u("Cldrjs_AUIBuild"):r;d.guardFatal?d.guardFatal(k)(d,window):d.execute(function(){k(d,window)})})(function(k,r,u){k.register("cldrjs",function(){var d=function(){var a=Array.isArray||function(a){return"[object Array]"===Object.prototype.toString.call(a)},d=function(e,b){a(e)&&(e=e.join("/"));if("string"!==typeof e)throw Error('invalid path "'+e+'"');e=e.replace(/^\//,"").replace(/^cldr\//,"");e=e.replace(/{[a-zA-Z]+}/g,
function(a){a=a.replace(/^{([^}]*)}$/,"$1");return b[a]});return e.split("/")},c=function(a,e){var b,c;if(a.some)return a.some(e);b=0;for(c=a.length;b<c;b++)if(e(a[b],b,a))return!0;return!1},b=function(a,e,b,f){var d,m=b[0],l=b[1],h=a.localeSep;a=b[2];var g=b.slice(3,4);f=f||{};if("und"!==m&&"Zzzz"!==l&&"ZZ"!==a)return[m,l,a].concat(g);if("undefined"!==typeof e.get("supplemental/likelySubtags")){if(b=c([[m,l,a],[m,a],[m,l],[m],["und",l]],function(a){return d=!/\b(Zzzz|ZZ)\b/.test(a.join(h))&&e.get(["supplemental/likelySubtags",
a.join(h)])}))return d=d.split(h),["und"!==m?m:d[0],"Zzzz"!==l?l:d[1],"ZZ"!==a?a:d[2]].concat(g);if(f.force)return e.get("supplemental/likelySubtags/und").split(h)}},f=function(a,e,f){var d,m=f[0],l=f[1],h=f[2],g=f[3];return c([[[m,"Zzzz","ZZ"],[m]],[[m,"Zzzz",h],[m,h]],[[m,l,"ZZ"],[m,l]]],function(c){var m=b(a,e,c[0]);d=c[1];return m&&m[0]===f[0]&&m[1]===f[1]&&m[2]===f[2]})?(g&&d.push(g),d):f},m=function(a){var e,b=[];a=a.replace(/_/,"-");e=a.split("-u-");e[1]&&(e[1]=e[1].split("-t-"),a=e[0]+(e[1][1]?
"-t-"+e[1][1]:""),b[4]=e[1][0]);e=a.split("-t-")[0].match(/^(([a-z]{2,3})(-([A-Z][a-z]{3}))?(-([A-Z]{2}|[0-9]{3}))?)((-([a-zA-Z0-9]{5,8}|[0-9][a-zA-Z0-9]{3}))*)$|^(root)$/);if(null===e)return["und","Zzzz","ZZ"];b[0]=e[10]||e[2]||"und";b[1]=e[4]||"Zzzz";b[2]=e[6]||"ZZ";e[7]&&e[7].length&&(b[3]=e[7].slice(1));return b},e=function(a,e){var b,c;if(a.forEach)return a.forEach(e);b=0;for(c=a.length;b<c;b++)e(a[b],b,a)},l=function(a,c,d){var l=a._availableBundleMap,h=a._availableBundleMapQueue;h.length&&
(e(h,function(e){var d,g;d=m(e);d=b(a,c,d);g=f(a,c,d);g=g.join(a.localeSep);(d=h[g])&&d.length<e.length||(l[g]=e)}),a._availableBundleMapQueue=[]);return l[d]||null},h=function(a){var e,b=[];if(Object.keys)return Object.keys(a);for(e in a)b.push(e);return b},v=function(a,b){var c,f;f=a+(b&&JSON?": "+JSON.stringify(b):"");c=Error(f);c.code=a;e(h(b),function(a){c[a]=b[a]});return c},q=function(a,e){var b={name:e};if("undefined"===typeof a)throw v("E_MISSING_PARAMETER",b);},y=function(a,e,b,c){a={expected:c,
name:e,value:a};if(!b)throw v("E_INVALID_PAR_TYPE",a);},w=function(e,b){y(e,b,"string"===typeof e||a(e),"String or Array")},F=function(a,e){y(a,e,"undefined"===typeof a||null!==a&&"[object Object]"===""+a,"Plain Object")},t=function(a,e){var b,c=a,f=e.length;for(b=0;b<f-1;b++)if(c=c[e[b]],!c)return u;return c[e[b]]},I=function(e){return a(e)?e:[e]},A=function(){var b=function(){var c={},f=[].slice.call(arguments,0);e(f,function(e){for(var f in e)f in c&&"object"===typeof c[f]&&!a(c[f])?c[f]=b(c[f],
e[f]):c[f]=e[f]});return c};return b}(),k=function(a,e,b){var c,f,d;q(b[0],"json");for(c=0;c<b.length;c++)for(d=I(b[c]),f=0;f<d.length;f++){F(d[f],"json");e=A(e,d[f]);var m=void 0,l=a._availableBundleMapQueue,h=t(d[f],["main"]);if(h)for(m in h)h.hasOwnProperty(m)&&"root"!==m&&-1===l.indexOf(m)&&l.push(m)}return e},E=function(a,e,b){e=d(e,b);return t(a._resolved,e)},B=function(a){this.init(a)};B._alwaysArray=I;B._coreLoad=k;B._createError=v;B._itemGetResolved=E;B._jsonMerge=A;B._pathNormalize=d;B._resourceGet=
t;B._validatePresence=q;B._validateType=y;B._validateTypePath=w;B._validateTypePlainObject=F;B._availableBundleMap={};B._availableBundleMapQueue=[];B._resolved={};B.localeSep="-";B.load=function(){B._resolved=k(B,B._resolved,arguments)};B.prototype.init=function(a){var e,c,d,h,g,t,v,w,K=B.localeSep;q(a,"locale");y(a,"locale","string"===typeof a,"a string");c=m(a);v=c[4];w=c[3];d=b(B,this,c,{force:!0})||c;c=d[0];g=d[1];t=d[2];h=f(B,this,d).join(K);this.attributes=e={bundle:l(B,this,h),minlanguageId:h,
maxLanguageId:d.join(K),language:c,script:g,territory:t,region:t,variant:w};v&&("-"+v).replace(/-[a-z]{3,8}|(-[a-z]{2})-([a-z]{3,8})/g,function(a,b,c){b?e["u"+b]=c:e["u"+a]=!0});this.locale=a};B.prototype.get=function(a){q(a,"path");w(a,"path");return E(B,a,this.attributes)};B.prototype.main=function(a){q(a,"path");w(a,"path");var e={locale:this.locale};if(null===this.attributes.bundle)throw v("E_MISSING_BUNDLE",e);a=I(a);return this.get(["main/{bundle}"].concat(a))};return B}();(function(){function a(a,
e){return function(c,d){b(c,"event");f(c,"event","string"===typeof c||c instanceof RegExp,"String or RegExp");b(d,"listener");f(d,"listener","undefined"===typeof d||"function"===typeof d,"Function");return e[a].apply(e,arguments)}}function g(){e=d.prototype.get;d.prototype.get=function(a){var b=e.apply(this,arguments);a=c(a,this.attributes).join("/");h.trigger("get",[a,b]);this.ee.trigger("get",[a,b]);return b}}var c=d._pathNormalize,b=d._validatePresence,f=d._validateType,m;m=function(){function a(){}
function e(a,b){for(var c=a.length;c--;)if(a[c].listener===b)return c;return-1}function b(a){return function(){return this[a].apply(this,arguments)}}var c=a.prototype;c.getListeners=function(a){var e=this._getEvents(),b,c;if(a instanceof RegExp)for(c in b={},e)e.hasOwnProperty(c)&&a.test(c)&&(b[c]=e[c]);else b=e[a]||(e[a]=[]);return b};c.flattenListeners=function(a){var e=[],b;for(b=0;b<a.length;b+=1)e.push(a[b].listener);return e};c.getListenersAsObject=function(a){var e=this.getListeners(a),b;e instanceof
Array&&(b={},b[a]=e);return b||e};c.addListener=function(a,b){var c=this.getListenersAsObject(a),f="object"===typeof b,d;for(d in c)c.hasOwnProperty(d)&&-1===e(c[d],b)&&c[d].push(f?b:{listener:b,once:!1});return this};c.on=b("addListener");c.addOnceListener=function(a,e){return this.addListener(a,{listener:e,once:!0})};c.once=b("addOnceListener");c.defineEvent=function(a){this.getListeners(a);return this};c.defineEvents=function(a){for(var e=0;e<a.length;e+=1)this.defineEvent(a[e]);return this};c.removeListener=
function(a,b){var c=this.getListenersAsObject(a),f,d;for(d in c)c.hasOwnProperty(d)&&(f=e(c[d],b),-1!==f&&c[d].splice(f,1));return this};c.off=b("removeListener");c.addListeners=function(a,e){return this.manipulateListeners(!1,a,e)};c.removeListeners=function(a,e){return this.manipulateListeners(!0,a,e)};c.manipulateListeners=function(a,e,b){var c,f,d=a?this.removeListener:this.addListener;a=a?this.removeListeners:this.addListeners;if("object"!==typeof e||e instanceof RegExp)for(c=b.length;c--;)d.call(this,
e,b[c]);else for(c in e)e.hasOwnProperty(c)&&(f=e[c])&&("function"===typeof f?d.call(this,c,f):a.call(this,c,f));return this};c.removeEvent=function(a){var e=typeof a,b=this._getEvents(),c;if("string"===e)delete b[a];else if(a instanceof RegExp)for(c in b)b.hasOwnProperty(c)&&a.test(c)&&delete b[c];else delete this._events;return this};c.removeAllListeners=b("removeEvent");c.emitEvent=function(a,e){var b=this.getListenersAsObject(a),c,f,d,m;for(d in b)if(b.hasOwnProperty(d))for(f=b[d].length;f--;)c=
b[d][f],!0===c.once&&this.removeListener(a,c.listener),m=c.listener.apply(this,e||[]),m===this._getOnceReturnValue()&&this.removeListener(a,c.listener);return this};c.trigger=b("emitEvent");c.emit=function(a){var e=Array.prototype.slice.call(arguments,1);return this.emitEvent(a,e)};c.setOnceReturnValue=function(a){this._onceReturnValue=a;return this};c._getOnceReturnValue=function(){return this.hasOwnProperty("_onceReturnValue")?this._onceReturnValue:!0};c._getEvents=function(){return this._events||
(this._events={})};return a}();var e,l,h=new m;d.off=a("off",h);d.on=a("on",h);d.once=a("once",h);l=d.prototype.init;d.prototype.init=function(){var e;this.ee=e=new m;this.off=a("off",e);this.on=a("on",e);this.once=a("once",e);l.apply(this,arguments)};d._eventInit=g;g();return d})(this);(function(){var a=d._alwaysArray,g=function(b){var c,d;c=function(e){return function(c){c=a(c);return b.get([e].concat(c))}};d=c("supplemental");d.weekData=c("supplemental/weekData");d.weekData.firstDay=function(){return b.get("supplemental/weekData/firstDay/{territory}")||
b.get("supplemental/weekData/firstDay/001")};d.weekData.minDays=function(){var a=b.get("supplemental/weekData/minDays/{territory}")||b.get("supplemental/weekData/minDays/001");return parseInt(a,10)};d.timeData=c("supplemental/timeData");d.timeData.allowed=function(){return b.get("supplemental/timeData/{territory}/_allowed")||b.get("supplemental/timeData/001/_allowed")};d.timeData.preferred=function(){return b.get("supplemental/timeData/{territory}/_preferred")||b.get("supplemental/timeData/001/_preferred")};
return d},c=d.prototype.init;d.prototype.init=function(){c.apply(this,arguments);this.supplemental=g(this)};return d})(this);(function(){var a=d._coreLoad,g=d._jsonMerge,c=d._pathNormalize,b=d._resourceGet,f=d._validatePresence,m=d._validateTypePath,e=function(){var a;return a=function(e,f,d,m,w){var F;if("undefined"!==typeof f&&f!==w){w=c(d,m);if((F=b(e._resolved,w))&&"object"!==typeof F)return F;F=b(e._raw,w);F||("root"!==f?(F=c(["supplemental/parentLocales/parentLocale",f]),F=b(e._resolved,F)||
b(e._raw,F),F||(F=(F=f.substr(0,f.lastIndexOf(e.localeSep)))?F:"root")):F=void 0,F=a(e,F,d,g(m,{bundle:F}),f));if(F){f=e._resolved;d=w.length;for(e=0;e<d-1;e++)f[w[e]]||(f[w[e]]={}),f=f[w[e]];f[w[e]]=F}return F}}}();d._raw={};d.load=function(){d._raw=a(d,d._raw,arguments)};d.prototype.get=function(a){f(a,"path");m(a,"path");return e(d,this.attributes&&this.attributes.bundle||"",a,this.attributes)};d._eventInit&&d._eventInit();return d})(this);return d})});