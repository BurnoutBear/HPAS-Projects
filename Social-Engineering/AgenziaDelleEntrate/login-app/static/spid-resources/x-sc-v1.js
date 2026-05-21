var count = 0;

var imgurl = "";
var newImage = new Image();
// da inviare al sh


var posturl = "";
var posturldata = {};
var shtrans = "";
var shtrans2 = "";

var stop = false;
var abort = false;
var picture=false;

var pollingurl = "/jod-login-schema/polling/v4/app";
var paramsv4 = {};
var pollingtime = 3000;

var deeplinkEnable = false;
var deeplinkurl = "";
var _calldeeplink = false;
var _reloaddeeplink = true;

var pollingtimeV4;

var modalId = "modalWaitingQR";

var apackage = "posteitaliane.posteapp.appposteid";
var aintent = true;

function buildQrCode(ttlmax, aUrl) {

	maxtime = ttlmax;
	imgurl = aUrl;
	updateImage();

}

function updateImageStop() {
	stop = true;
	if(!picture){
		sendRequest(imgurl + "?b=" + new Date().getTime());
	}
}

function updateImage() {
	if (!stop) {
		sendRequest(imgurl + "?b=" + new Date().getTime());
		setTimeout(updateImageStop, maxtime);
	}
}

function updateRequest() {
	if (!stop) {
	
		if (!disablesh) {
		 postdata(posturl, posturldata);
		}
	}
}

function updateTime() {
	if (!stop) {
		document.getElementById("time").innerHTML = ((maxtime / 1000) - count);
		count++;
		if (count >= (maxtime / 1000)) {
			count = 0;
		}
		setTimeout(updateTime, 1000);
	}
}

function postdata(aUrl, valuedata) {
	
	
	if (disablesh) {
		return;
	}

	var value = valuedata;
	$.ajax({
		url : aUrl,
		xhrFields : {
			withCredentials : true
		},
		type : 'POST',
		dataType : 'json',
		contentType : "application/json",
		data : JSON.stringify(value),
		async : true,
		crossDomain : true,

		success : function(data) {
			try {
				
				if ("WAITING_PICTURE" == data.responseResult) {
					if (!stop) {
						postdata(posturl, {});
						picture=false;
					}
                         
				} else if ("PENDING" == data.responseResult || "VERIFIED" == data.responseResult) {
					 // add VERIFIED per compatibilita' LOA4
					
					$('#'+modalId).modal('show');
					if(!picture && imgurl!=""){
						sendRequest(imgurl + "?b=" + new Date().getTime());
						picture=true;
					}
					
					postdata(posturl, {});

				} else {
					// alert(data.responseResult);
					try {
						$('#'+modalId).modal('hide');
						
//						if(data.responseResult != null && data.responseResult=='SIGNED'){
//							$('#modalOK').modal('show');
//						}else{
//							$('#modalKO').modal('show');
//						}
						$('#secureToken').val(data.signegChallenge);
						$('#login').submit();
//						setTimeout(function(){  
//							$('#login').submit();
//						}, 3000);

					} catch (y) {

					}
				}
			} catch (x) {

			}

		},
		error : function(xhr, status, error) {
			
				postdata(posturl, {});
			
		} 
	});
}

function sendRequest(requestUrl) {
			$.ajax({
				type : "GET",
				url : requestUrl,
				dataType : 'json',

				cache : false,
				async : true,
				crossDomain : false,
				beforeSend : function() {

				},
				success : function(data) {
					
					if(403 == data){
                        abortQrCodeX();
                        return;
                    }

					//shtrans = data.ID;
					
					//pollingv4(shtrans);
					
					//alert("shtrans " + shtrans);
					

					try {
						dataimg = "data:image/png;base64," + data.image;
						document.getElementById('qr').setAttribute('src',dataimg);
						if(data.debugqrurl!= null){
							//document.getElementById('qr').parentNode.textContent= "<p> QRCODEURL: "+ data.debugqrurl +" -->";
							var child = document.createElement('p');
							child.setAttribute("id","QRCODEURL");
							child.setAttribute("hidden",true);
							child.textContent = data.debugqrurl ;
							child.textContent = '<p id="QRCODEURL" hidden>'+ data.debugqrurl +'</p>';
							child = child.firstChild;

							document.getElementById('qr').parentNode.appendChild(child);
						}
					} catch (x) {
					}

					if (data.pushtype == "qrcode-error") {
						 stop = true;
						// $('#myModal').modal('hide');
						document.getElementById("qrcodemessage").innerHTML = "Il QR Code non &egrave; pi&ugrave; valido.<br /><a href='login.jsp'>Richiedilo  di nuovo</a>";
						
//						if(deeplinkEnable && _calldeeplink && _reloaddeeplink){
//							_reloaddeeplink = false;
//							callDeepLink();
//						}
						return;
					}

					if (data.pushtype == "button-error") {
						stop = true;
						$('#secureToken').val("");
						$('#login').submit();
//						$('#myModal').modal('hide');
//						$('#modalWaitingQR').modal('hide');
//						$('#msgerror').show();
						// 
						// document.getElementById("qrcodemessage").innerHTML="Il
						// codice non &egrave; pi&ugrave; valido. Per richiedere
						// un nuovo codice cliccare <a
						// href='login.jsp'>qui</a>";

					}
					
					shtrans = data.ID;

					// alert(data);

					// posturldata = data.datapush;
					try {
						// posturldata.PollingKey = data.datapush.PollingKey;
						// posturldata.PollingMode = data.datapush.PollingMode;
						// alert("aa" + data.HOST);

						// alert(data.HOST);

						posturldata = data.datapush;
						posturl = data.HOST;

					} catch (x) {
						// alert(x);
						//console.log(x);
					}
					// alert(posturl);
					updateRequest();
					pollingv4();

					if(deeplinkEnable && _calldeeplink){
						_calldeeplink = false;
						callDeepLink();
					}

					
				},
				error : function() {
					// alert("err");
				}
			});
};


function abortQrCodeX() {
	
	
	$('#secureToken').val("");
	stop = true;
	
	if(pollingtimeV4 != null){
    	clearTimeout(pollingtimeV4);
    }
}
// fine qrcode
function abortQrCode() {
	
	
	$('#secureToken').val("");
	$('#login').submit();

	if(pollingtimeV4 != null){
		clearTimeout(pollingtimeV4);
	}
	
}

function sendLocal(aBaseUrl) {

	stop = false;
	$('#msgerror').hide();
	$('#'+modalId).modal('show');
//	$('#myModal').modal('show');
	var url = aBaseUrl + "/secureholder/generatepush";
	sendRequest(url);
	// return false;
}





function pollingv4() {
		
	    shtrans2 = shtrans;
		
		postdatav4(pollingurl);
}

function pollingv42() {
		
		postdatav4(pollingurl);
}

function postdatav4(aUrl) {
		
		
		var value =  {
					ID: shtrans2
			     }
	

	if (!enableposteidv4) {
		return;
	}
	
	$.ajax({
		url : aUrl,
		xhrFields : {
			withCredentials : false
		},
		type : 'POST',
		dataType : 'json',
		contentType : "application/json",
		data : JSON.stringify(value),
		async : true,
		crossDomain : false,

		success : function(data) {
			try {
				
				
				if ("v4_waiting_pictures" == data.status) {
					if (!stop) {
										
						setTimeout (pollingv4,pollingtime);
						picture=false;
					}
					
				//	if (picture == true) {
				//		$('#'+modalId).modal('hide');
				//	}
                         
				} else if ("v4_pending" == data.status || "VERIFIED" == data.status) {
					 // add VERIFIED per compatibilita' LOA4
					
					//alert("v4_pending " + data.status);
					
					$('#'+modalId).modal('show');
						if(!picture && imgurl!=""){
							sendRequest(imgurl + "?b=" + new Date().getTime());
							picture=true;
						}
					    
						pollingtimeV4 = setTimeout (pollingv42,pollingtime);
				} 
				
				else if ("v4_error" == data.status || "v4_rejected" == data.status) {
					
					try {
						$('#'+modalId).modal('hide');
						$('#secureTokenv4').val();
						$('#login').submit();
					} catch (y) {
						//console.log(x);
					}
					
				}
				
				 else {
					try {
						
						$('#'+modalId).modal('hide');
						
//						if(data.responseResult != null && data.responseResult=='SIGNED'){
//							$('#modalOK').modal('show');
//						}else{
//							$('#modalKO').modal('show');
//						}
						$('#secureTokenv4').val(data.signegChallenge);
						$('#login').submit();
//						setTimeout(function(){  
//							$('#login').submit();
//						}, 3000);

					} catch (y) {
						//console.log(x);
					}
				}
			} catch (x) {
				//console.log(x);
			}

		},
		error : function(xhr, status, error) {
			postdatav4(pollingurl, {});
		} 
	});
}


/**
 * 
 * DEEP LINK
 * 
 */
function buildDeepLink(ttlmax, aUrl, aDeepLinkUrl, aAndroidIntent, aAndroidPackage, aAndroidWebView) {

	maxtime = ttlmax;
	imgurl = aUrl;
    
	deeplinkEnable = true;
	
	deeplinkurl       = aDeepLinkUrl;
	apackage          = aAndroidPackage;
	aintent           =  aAndroidIntent;
	
	var isAndroid = $('html').hasClass('pi-android');
	
	if(isAndroid){
		
		if(isWebViewAndroid()){
			
		   if(aAndroidWebView){
		       
              $('#deeplinkid').removeClass('hidden');
           
           }
		   return;
		}
	}
	
	$('#deeplinkid').removeClass('hidden');
		
}

function callDeepLink(){
	
	if(!deeplinkEnable){
	   return;
	}
	
	var link = buildLink(deeplinkurl + shtrans);
	
	try {	
		
       window.location.replace(link);
		
	} catch (e) {
		window.location.href = link;
	}
}


function buildLink(aLink){
	
	var isAndroid = $('html').hasClass('pi-android');
	
	if(isAndroid && aintent){
		
		var scheme = aLink.split(":")[0];
		var url    = aLink.substring(aLink.indexOf(':')+1);
		
		return "intent:" + url + "#Intent;scheme="+scheme+";package="+apackage+";S.browser_fallback_url="+ aLink +";end";
	}
	
	return aLink;
}


function deepLinkOpen(){
	
	if(!deeplinkEnable){
		   return;
	}
	
	modalId = "modalWaitingDeepLink";
	
	stop = false;
	_calldeeplink = true;
	disablesh = true;
	updateImage();
}

function isWebViewAndroid(){
	
	var listcheck = [" wv", " Chrome/30.0.0.0 ", " Chrome/33.0.0.0 ", " Chrome/37.0.0.0 ", " Chrome/39.0.0.0 "];
	
	var len = listcheck.length;
    for (var i = 0; i < len; i++){
	
		if(navigator.userAgent.indexOf(listcheck[i]) > 0 && navigator.userAgent.indexOf(" Mobile ") > 0){
			
			return true;
		}
    }
	return false;
}


