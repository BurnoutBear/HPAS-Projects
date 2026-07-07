/*****************************************************

    Utilita.js - (c) Poste Italiane 2016 - GD//FS//DU

*****************************************************/
/*  Set Browser-sniffing on/off */
var browserCheck = "on";
/*  Set Mediaquery-sniffing on/off */
var mqCheck = "on";
/*  Set Debug on/off */
var debugging = "off";
/*  Set Overlay pageLoader on/off */
var overlayPageLoad = "on"

/* Doc. Debug var on/off - USAGE:
 *       writeLog("----");
 *       writeWarning("ops");
 *       writeError("ops");
 *       writeInfo("ops");
 */

/* Doc. Mediaquery-sniffing var on/off - USAGE:
 *    class = 'pi-xs'
 *            'pi-sm'
 *            'pi-md'
 *            'pi-lg'
 */

/* Doc. Browser-sniffing class on html var on/off  
 *    class = 'pi-mobile'
 *            'pi-mobile pi-android'
 *            'pi-mobile pi-ios'
 *            'pi-firefox'
 *            'pi-ie pi-ie-edge'
 *            'pi-ie pi-ie10'
 *            'pi-ie pi-ie9'
 *            'pi-ie pi-ie8'
 *            'pi-ie pi-ie7'
 *            'pi-ie pi-ie6'
 *            'pi-chrome'
 *            'pi-opera'
 *            'pi-safari'
 */





/******************/

/* set log */

/******************/
function writeLog(arg) {
    if ((typeof console != "undefined") && (debugging == "on")) {
        console.log(arg);
    }
}

function writeError(arg) {
    if ((typeof console != "undefined") && (debugging == "on")) {
        console.error(arg);
    }
}

function writeInfo(arg) {
    if ((typeof console != "undefined") && (debugging == "on")) {
        console.info(arg);
    }
}

function writeWarning(arg) {
    if ((typeof console != "undefined") && (debugging == "on")) {
        console.warn(arg);
    }
}


/******************/

/* Media Query check */

/******************/

var mq_WindowWidth = $(window).width();
var mq_Detect = 'nomQDetect';


if (mqCheck == "on") {
    mqCheckDetection();
}

$(window).resize(function () {
    if (mqCheck == "on") {
        mqCheckDetection();
    }
});

function mqCheckDetection(mq_WindowWidth) {
    if ((mq_WindowWidth == null) || (mq_WindowWidth == '') || (mq_WindowWidth == 'undefined')) {
        var mq_WindowWidth = $(window).width();
    }
    if (mq_WindowWidth < 768) {
        if (!($('html').hasClass('pi-xs'))) {
            $('html').removeClass('pi-sm pi-md pi-lg');
            $('html').addClass('pi-xs');
            writeInfo('MediaQuery Check : ' + 'xs');
            mq_Detect = 'xs';
            return mq_Detect;
        }
    } else if ((mq_WindowWidth > 767) && (mq_WindowWidth < 992)) {
        if (!($('html').hasClass('pi-sm'))) {
            $('html').removeClass('pi-xs pi-md pi-lg');
            $('html').addClass('pi-sm');
            writeInfo('MediaQuery Check : ' + 'sm');
            mq_Detect = 'sm';
            return mq_Detect;
        }
    } else if ((mq_WindowWidth > 991) && (mq_WindowWidth < 1200)) {
        if (!($('html').hasClass('pi-md'))) {
            $('html').removeClass('pi-xs pi-sm pi-lg');
            $('html').addClass('pi-md');
            writeInfo('MediaQuery Check : ' + 'md');
            mq_Detect = 'md';
            return mq_Detect;
        }
    } else if ((mq_WindowWidth > 1199)) {
        if (!($('html').hasClass('pi-lg'))) {
            $('html').removeClass('pi-xs pi-sm pi-md');
            $('html').addClass('pi-lg');
            writeInfo('MediaQuery Check : ' + 'lg');
            mq_Detect = 'lg';
            return mq_Detect;
        }
    }
}

/******************/

/* Sniffing pixel density */

/******************/
function isHighDensity() {
    return ((window.matchMedia && (window.matchMedia('only screen and (min-resolution: 124dpi), only screen and (min-resolution: 1.3dppx), only screen and (min-resolution: 48.8dpcm)').matches || window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 1.3), only screen and (-o-min-device-pixel-ratio: 2.6/2), only screen and (min--moz-device-pixel-ratio: 1.3), only screen and (min-device-pixel-ratio: 1.3)').matches)) || (window.devicePixelRatio && window.devicePixelRatio > 1.3));
}


function isRetina() {
    return ((window.matchMedia && (window.matchMedia('only screen and (min-resolution: 192dpi), only screen and (min-resolution: 2dppx), only screen and (min-resolution: 75.6dpcm)').matches || window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 2), only screen and (-o-min-device-pixel-ratio: 2/1), only screen and (min--moz-device-pixel-ratio: 2), only screen and (min-device-pixel-ratio: 2)').matches)) || (window.devicePixelRatio && window.devicePixelRatio >= 2)) && /(iPad|iPhone|iPod)/g.test(navigator.userAgent);
}

/******************/

/* Modal recalc position (to center) */

/******************/
$(function () {
    function reposition() {
        var modal = $(this),
            dialog = modal.find('.modal-dialog');
        modal.css('display', 'block');

        // Dividing by two centers the modal exactly, but dividing by three 
        // or four works better for larger screens.
        dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
    }
    // Reposition when a modal is shown
    $('.modal').on('show.bs.modal', reposition);
    // Reposition when the window is resized
    $(window).on('resize', function () {
        $('.modal:visible').each(reposition);
    });
});



/******************/

/* Sniffing browser */

/******************/


if (browserCheck == "on") {
    BrowserDetection();
}


function BrowserDetection() {
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        writeInfo('Mobile Browser detected');
        //document.getElementsByTagName('html')[0].className += 'pi-mobile';
        $('html').addClass('pi-mobile');
        if (/Android/i.test(navigator.userAgent)) {
            writeInfo('Android Browser detected');
            //document.getElementsByTagName('html')[0].className += ' ' + 'pi-android';
            $('html').addClass('pi-android');
        } else if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) {
            writeInfo('Ios Browser detected');
            //document.getElementsByTagName('html')[0].className += ' ' + 'pi-ios';
            $('html').addClass('pi-ios');
        }
    } else if (/Firefox[\/\s](\d+\.\d+)/.test(navigator.userAgent)) {
        var ffversion = new Number(RegExp.$1);
        writeInfo('Firefox Browser detected');
        //document.getElementsByTagName('html')[0].className += 'pi-firefox';
        $('html').addClass('pi-firefox');

    } else if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)) {
        var ieversion = new Number(RegExp.$1);
        if (ieversion == 10) {
            // for IE10
            //document.getElementsByTagName('html')[0].className += 'pi-ie pi-ie10';
            $('html').addClass('pi-ie pi-ie10');
            writeInfo('IE10 Browser detected');
        } else if (ieversion == 9) {
            // for IE9
            //document.getElementsByTagName('html')[0].className += 'pi-ie pi-ie9';
            $('html').addClass('pi-ie pi-ie9')
            writeInfo('IE9 Browser detected');
        } else if (ieversion == 8) {
            // for IE8
            //document.getElementsByTagName('html')[0].className += 'pi-ie pi-ie8';
            $('html').addClass('pi-ie pi-ie8')
            writeInfo('IE8 Browser detected');
        } else if (ieversion == 7) {
            // for IE7
            //document.getElementsByTagName('html')[0].className += 'pi-ie pi-ie7';
            $('html').addClass('pi-ie pi-ie7')
            writeInfo('IE7 Browser detected');
        } else if (ieversion == 6) {
            // for IE6
            //document.getElementsByTagName('html')[0].className += 'pi-ie pi-ie6';
            $('html').addClass('pi-ie pi-ie6')
            writeInfo('IE6 Browser detected');
        }
    } else if (/Trident.*rv[ :]?[1-9]{2}\./.test(navigator.userAgent)) {
        var ieVersion = new Number(RegExp.$1);
        //document.getElementsByTagName('html')[0].className += 'pi-ie pi-ie-edge';
        $('html').addClass('pi-ie pi-edge');
        writeInfo('IE > 10 Browser detected');
    } else if (/Chrome[\/\s](\d+\.\d+)/.test(navigator.userAgent)) {
        var chromeversion = new Number(RegExp.$1);
        //document.getElementsByTagName('html')[0].className += 'pi-chrome';
        $('html').addClass('pi-chrome');
        writeInfo('Chrome Browser detected');
    } else if (/Opera[\/\s](\d+\.\d+)/.test(navigator.userAgent)) {
        var oprversion = new Number(RegExp.$1);
        //document.getElementsByTagName('html')[0].className += 'pi-opera';
        $('html').addClass('pi-opera');
        writeInfo('Opera Browser detected');
    } else if (/Safari[\/\s](\d+\.\d+)/.test(navigator.userAgent)) {
        var safariversion = new Number(RegExp.$1);
        //document.getElementsByTagName('html')[0].className += 'pi-safari';
        $('html').addClass('pi-safari');
        writeInfo('Safari Browser detected');
    }
}



/******************/

/* equalize element*/
/* setta altezza di una map / array a quella maggiore, in ingresso prende il selettore css */

/******************/


function pari_altezza_func(sel) {
    if ($(sel).length > 0) {
        var heights = $(sel).map(function () {
                return $(this).outerHeight();
            }).get(),


            maxHeight = Math.max.apply(null, heights);


        $(sel).css("min-height", maxHeight + 1);


        if ((mq_Detect == 'xs') && !($(sel).parents().hasClass('content-overflow'))) {
            $(sel).css("min-height", "auto");
        }

        if ($(sel).hasClass('equalize-height')) {
            $(sel).css("height", maxHeight + 1);
        }

        return maxHeight;
        //writeLog("equalize function: set minHeight to : " + maxHeight + " +1px on " + sel);
    }

}


function pari_altezza(myvar) {
    $(document).ready(function () {
        //writeLog("equalize function onLoad: called on " + myvar);
        pari_altezza_func(myvar);
        //writeLog("----");
    });



    var myidEq;
    $(window).resize(function () {
        clearTimeout(myidEq);
        myidEq = setTimeout(doneResizingEqualize, 350);
    });


    function doneResizingEqualize() {
        writeLog('reset min-height: ' + myvar);
        $(myvar).css("min-height", "auto");
        if ($(myvar).hasClass('equalize-height')) {
            $(myvar).css("height", "auto");
        }
        //writeLog("equalize function onResize: called on " + myvar);
        //writeLog("----");
        pari_altezza_func(myvar);

    }
}



/* ciclo equalize su elementi di una stessa riga ----- pari_altezza(".equalize* .panel-cards") */
function equalizeCycle(myclass, mycardclass) {
    //writeLog("----");
    var mynumMaxGruppiElementiEqualize = $(myclass).length;
    //writeLog("equalizeCycle function: trovati " + mynumMaxGruppiElementiEqualize + " gruppi di elementi");

    for (var i = 1; i <= mynumMaxGruppiElementiEqualize; i++) {
        var tgtcycle = myclass + "-" + i + " " + mycardclass;
        if ($(tgtcycle).length > 0) {
            pari_altezza(tgtcycle);
            //writeLog("Applico equalize su gruppi di elementi: " + tgtcycle);
        }
    }
    //writeLog("----");
}




$('ul.dropdown-menu.mega-dropdown-menu').on('click', function (event) {
    // The event won't be propagated up to the document NODE and 
    // therefore delegated events won't be fired
    event.stopPropagation();
});
