$(document).ready(function () {

    function getWeather(place) {
        $.ajax({
            url: links.get_weather,
            method: 'GET',
            data: {
                query: place
            },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    updateInfo(response.data);
                };
            },
            error: function(xhr, status, error) {
                console.error('Ошибка:', error);
            }
        })
    };

    function updateInfo(data) {
        const current = data.current;
        const near = data.hourly;   
        const $soonWeatherContainer = $('#soonWeatherContainer');

        $('#currentTemp').text(current.current_temp);
        $('#currentFeelTemp').text(current.current_feel_temp);
        $('#currentHumidity').text(current.current_humidity);
        $('#currentPressure').text(current.current_pressure);
        $('#currentPrecipitation').text(current.current_precipitation);

        $soonWeatherContainer.empty();
        for (let i = 0; i <= 3; i++) {
            $soonWeatherContainer.append(
                `<div data-id="${i}" class="hour-weather flex-1 rounded-lg border p-1">
                    <p>Температура: ${near[i].temp}°С</p>
                    <p>Ощущается как: ${near[i].feeltemp}°С</p>
                    <p>Влажность: ${near[i].humidity}%</p>
                    <p>Атмосферное давление: ${near[i].pressure}hPa</p>
                    <p>Вероятность осадков: ${near[i].precipitation}%</p>
                    <p>Скорость ветра: ${near[i].wind}м/с</p>
                </div>`
            );
        }
        $('#currentWeatherContainer').show();
        $('#futureWeatherContainer').show();
    }

    $('#searchInput').keydown(function (e) { 
        if (e.key === 'Enter') {
            getWeather($(this).val());
        }
    });

    $('#placesList').on('click', 'li', function() {
        getWeather($(this).text());
        $('#searchInput').val('');
        $('#placesList').empty();
        $('#searchInputClear').hide();  
    })

    $('#searchInputClear').click(function() {
        $('#placesList').empty();
        $('#searchInput').val('').focus();
        $(this).hide();
    })

    $('#searchInput').on('input', function(){

        if ($(this).val().length > 0) {
            $('#searchInputClear').show();
        }
        else {
            $('#searchInputClear').hide();
        }
    })

});