$(document).ready(function () {

    let history = $('#placesList li').map(function() {
        return $(this).text();
    }).get();

    function getWeather(place) {
        if (!place) return;
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
                    history = response.history;
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
                `<div data-id="${i}" class="hour-weather">
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
    };

    function updateList(cities) {
        const $list = $('#placesList');
        $list.empty();
        cities.forEach(function(city) {
            $list.append(`<li class="autocomplete-list-item">${city}</li>`)
        })
    }

    function getCities(query) {
        $.ajax({
            url: links.get_cities,
            method: 'GET',
            data: {
                'query': query.trim()
            },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    updateList(response.cities);
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка:', error);
            }
        })
    };



    $('#searchInput').keydown(function (e) { 
        if (e.key === 'Enter') {
            getWeather($(this).val());
        }
    });

    $('#placesList').on('click', 'li', function() {
        getWeather($(this).text());
        $('#searchInput').val($(this).text());
        $('#placesList').empty();
        $('#searchInputClear').show();  
    })

    $('#searchInputClear').click(function() {
        $('#placesList').empty();
        $('#searchInput').val('').focus();
        $(this).hide();
        history.forEach(function(place) {
            $('#placesList').append(`<li class="autocomplete-list-item">${place}</li>`)
        })
    })

    $('#searchInput').on('input', function(){

        let query = $(this).val();

        if (query.length > 0) {
            $('#searchInputClear').show();
            getCities(query);
        }
        else {
            $('#searchInputClear').hide();
        }

    })

});