$("#values1").change(function () {
    input_check(this, () => {
        let endpoint = '/api/calculate_coin_amount';
        if ($(this).val() !== '') {
            $("#values2").addClass("loading");
            $.ajax({
                method: "POST",
                url: endpoint,
                data: {'amount': $(this).val(), 'from': "DENCH", 'to': $('#ex_type').val()},
                success: function (data) {
                    let values2 = $("#values2")
                    values2
                        .val(data.amount)
                        .removeClass("loading");
                    if(values2.val() !== '0') {
                        $(".buy-btn.trade-button").removeClass('disabled');
                    }
                    else {
                        $(".buy-btn.trade-button").addClass('disabled');
                    }
                },
                error: function (error_data) {
                    console.log(error_data);
                }
            })
        } else {
            $(".buy-btn.trade-button").addClass('disabled');
        }
    });
});

let value2 = $('#values2') ;
value2.change(function () {
    input_check(this, () => {
        let endpoint = '/api/calculate_coin_amount';
        if ($(this).val() !== '') {
            $('#values1').addClass('loading');
            $.ajax({
                method: 'POST',
                url: endpoint,
                data: {'amount': $(this).val(), 'from': $('#ex_type').val(), 'to': "DENCH"},
                success: function (data) {
                    let values1 = $('#values1')
                    values1
                        .val(data.amount)
                        .removeClass('loading');
                    if(values1.val() !== '0') {
                        $(".buy-btn.trade-button").removeClass('disabled');
                    }
                    else {
                        $(".buy-btn.trade-button").addClass('disabled');
                    }
                },
                error: function (error_data) {
                    console.log(error_data);
                }
            })
        } else {
            $(".buy-btn.trade-button").addClass('disabled');
        }
    });
});


$(".trade-button.buy-btn").on('click', function () {
    let hash = "<div id='wallet-hash-wrapper'><span id='wallet-hash' title='Click to copy'>0xa1e453b2c576acEEA6d406b7366536feB8A6DF55</span></div><div class='buy-btn confirm-button' id='confirm-btn'><span style='color: #212529'>CONFIRM</span></div>",
        that = $(this);
    $('<p id="countdown-timer">1 m 59 s</p>' + hash).insertBefore($(this));
    $(this).hide();
    $('#values1').prop('disabled', true);
    $('#wallet-hash-wrapper').on('click', function () {
        copyToClipboard($(this).text());
    });


    // Set the date we're counting down to
    let countDownDate = new Date().getTime() + 120000;

    // Update the count down every 1 second
    let x = setInterval(function () {

        // Get today's date and time
        let now = new Date().getTime();

        // Find the distance between now and the count down date
        let distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="demo"
        if ($("#countdown-timer").length < 1) {
            clearInterval(x);
            return;
        }
        let string = document.getElementById("countdown-timer").innerHTML;
        if (string.includes('m ')) {
            document.getElementById("countdown-timer").innerHTML = minutes + "m " + seconds + "s";
        }

        // If the count down is over, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("countdown-timer").innerHTML = "EXPIRED";
            setTimeout(function () {
                $("#wallet-hash, #countdown-timer, #wallet-hash-wrapper").remove();
                $('.confirm-button').remove();
                that.show();
            }, 1500);
        }
    }, 1000);

    $(".confirm-button.buy-btn").on('click', function () {
        let endpoint = '/api/transaction';
        $(".confirm-button.buy-btn").addClass('disabled');
        $.ajax({
            method: "POST",
            url: endpoint,
            data: {
                'coin_amount': document.getElementById('values1').value,
                'expected_coin': $('#ex_type').val(),
                'chain_type': $('#chain_type').val()
            },
            success: function (data) {
                document.getElementById("countdown-timer").innerHTML = data.response;
                setTimeout(function () {
                    $("#wallet-hash, #countdown-timer, #wallet-hash-wrapper").remove();
                    $('.confirm-button').remove();
                    $(".trade-button.buy-btn").show();
                }, 4000);
                console.log(data);
            },
            error: function (error_data) {
                console.log(error_data);
            }
        });
    });

    function copyToClipboard(text) {
        let sampleTextarea = document.createElement("textarea");
        document.body.appendChild(sampleTextarea);
        sampleTextarea.value = text; //save main text in it
        sampleTextarea.select(); //select textarea contenrs
        document.execCommand("copy");
        document.body.removeChild(sampleTextarea);
    }
});

let exchange_type = $('#ex_type');
let option_erc = ['USDT', 'USDC', 'DODO'];
let option_bep = ['BUSD', 'CAKE', 'DODO'];

setSelectOptions(option_bep, exchange_type);

$("#chain_type").on('change', function () {
    let option = option_bep;
    if (parseInt($(this).val()) === 1) {
        option = option_bep;
    } else if (parseInt($(this).val()) === 2) {
        option = option_erc;
    }
    setSelectOptions(option, exchange_type);
});

function setSelectOptions(options, element) {
    let html_to_add = '';
    for (let i = 0; i < options.length; i++) {
        html_to_add = html_to_add + '<option value=' + options[i] + '>' + options[i] + '</option>'
    }
    element.html(html_to_add);
    element.val(options[0]);
    value2.attr('placeholder', options[0]);
    $('#values1').attr('min', 0);
}

exchange_type.on('change', function () {
    $('#values2').attr('placeholder', $(this).val());
});


function input_check(that, callback) {
    let contract_type = $('#chain_type');
    if (parseInt(contract_type.val()) === 1) {
        that.value = Math.abs(that.value);
        callback();
    } else if (parseInt(contract_type.val()) === 2) {
        let min_quote = 1000;
        if (that.id === 'values1') {
            let endpoint = '/api/calculate_coin_amount';
            $.ajax({
                method: "POST",
                url: endpoint,
                data: {'amount': min_quote, 'from': exchange_type.val(), 'to': "DENCH"},
                success: function (data) {
                    if (parseFloat(data.amount) > that.value) {
                        that.value = parseFloat(data.amount);
                    }
                    callback();
                },
                error: function (error_data) {
                    console.log(error_data);
                }
            });
        } else if (that.id === 'values2') {
            if (min_quote > that.value) {
                that.value = min_quote;
            }
            callback();
        }
    }

}
