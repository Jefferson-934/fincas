

$(function () {
    let map;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getCoords, getError)
    } else {

    }

    function getCoords(position) {
        let lat = position.coords.latitude;
        let long = position.coords.longitude;
        initMap(lat, long);
    }

    function getError(err) {

        initMap(13.30272, -87.194107);
    }
    function initMap(lat, long) {

        let latlong = new google.maps.LatLng(lat, long);
        let mapSettings = {
            center: latlong,
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }

        map = new google.maps.Map(document.getElementById("mapa"), mapSettings);
        let marker = new google.maps.Marker({
            position: latlong,
            map: map,
            draggable: true,
            title: "Arrastrame"
        });

        google.maps.event.addListener(marker, "position_changed", function () {
            getMarkerCoords(marker);
        })
    }

    function getMarkerCoords(marker) {
        var marketCoords = marker.getPosition();
        $("#latitud").val(marketCoords.lat())
        $("#longitud").val(marketCoords.lng())
    }




});





function eliminar(path,id) {
    //console.log(id)           
    Swal.fire({
        title: 'Estas seguro de eliminar?',
        text: "Se borrará de forma permanente!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si eliminar'
    }).then(function (result) {
        if (result.isConfirmed) {
            window.location.href = path + id + "/"

        }
    })
}

function eliminar_temp(path,id) {
    //console.log(id)           
    Swal.fire({
        title: 'Estas seguro de eliminar?',
        text: "Se desactivará el registro!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Eliminar'
    }).then(function (result) {
        if (result.isConfirmed) {
            window.location.href = path + id + "/"

        }
    })
}




function activar(path,id) {
    //console.log(id)           
    Swal.fire({
        title: 'Desea activar esta finca?',
        text: "Se activará nuevamente la finca!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si activar'
    }).then(function (result) {
        if (result.isConfirmed) {
            window.location.href = path + id + "/"

        }
    })
} 

function activar_u(path,id) {
    //console.log(id)           
    Swal.fire({
        title: 'Desea activar este registro?',
        text: "Se activará nuevamente el registro!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si activar'
    }).then(function (result) {
        if (result.isConfirmed) {
            window.location.href = path + id + "/"

        }
    })
} 


$(document).ready(function(){
	var altura = $('.navbar').offset().top;
	
	$(window).on('scroll', function(){
		if ( $(window).scrollTop() > altura ){
			$('.navbar').addClass('menu-fixed');
		} else {
			$('.navbar').removeClass('menu-fixed');
		}
	});

});



/* login*/


