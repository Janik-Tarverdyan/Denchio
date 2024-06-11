
const exchange_type = $('#ex_type');
const chain_type = $('#chain_type');
const chain_options = {
    "MATIC": chain_type.data('matic'),
    "ERC": ['USDT', 'USDC', 'DODO'],
    "BEP": ['BUSD', 'CAKE', 'DODO'],
}
const value1 = $('#values1');
const value2 = $('#values2');
const buyDenchDiv = $('.buy-dench')
var canDoInput = true

var typingTimer;
var doneTypingInterval = 500;

chain_type.on("change", (e) => {
    setSelectOptions(chain_options[chain_type.val()], exchange_type)
})

setSelectOptions(chain_options[chain_type.val()], exchange_type);

function setSelectOptions(options, element) {
    let html_to_add = '';
    for (let i = 0; i < options.length; i++) {
        html_to_add += `<option value="${options[i].id}" data-symbol="${options[i].symbol}">${options[i].name}</option>`
    }
    element.html(html_to_add);
    element.val(options[0].id);
    value2.attr('placeholder', options[0].symbol);
    $('#values1').attr('min', 0);
}

exchange_type.on('change', function () {
    $('#values2').attr('placeholder', chain_options[chain_type.val()].filter((elem) => elem.id == $(this).val())[0].symbol);
    doneTyping2()
});

value1.on('keyup', function () {
    if (canDoInput) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping1, doneTypingInterval);
    }
});

value1.on('keydown', function (e) {
    if (!canDoInput) {
        e.preventDefault()
    } else {
        clearTimeout(typingTimer);
    }
});

function doneTyping1() {
    const value = value1.val()
    const endpoint = '/api/calculate_coin_amount';
    if (!!value) {
        canDoInput = false
        buyDenchDiv.css('opacity', 0.8)
        buyDenchDiv.css('pointer-events', 'none')
        $.ajax({
            method: 'GET',
            url: endpoint,
            data: {'amount': value, 'to': $('#ex_type').val(), 'from': "DENCH"},
            success: function (data) {
                value2
                    .val(data.amount)
                    .removeClass('loading');
                if(value2.val() !== '0') {
                    $(".buy-btn.trade-button").removeClass('disabled');
                    setBuyDenchButtonURL(data.swap_url)
                }
                else {
                    $(".buy-btn.trade-button").addClass('disabled');
                }
            },
            error: function (error_data) {
                console.log(error_data);
            }
        }).done((e) => {
            buyDenchDiv.css('opacity', 1)
            buyDenchDiv.css('pointer-events', 'unset')
            canDoInput = true
        })
    }
}

value2.on('keyup', function () {
    if (canDoInput) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping2, doneTypingInterval);
    }
});

value2.on('keydown', function (e) {
    if (!canDoInput) {
        e.preventDefault()
    } else {
        clearTimeout(typingTimer);
    }
});

function doneTyping2() {
    const value = value2.val()
    const endpoint = '/api/calculate_coin_amount';
    if (!!value) {
        canDoInput = false
        buyDenchDiv.css('opacity', 0.8)
        buyDenchDiv.css('pointer-events', 'none')
        $.ajax({
            method: 'GET',
            url: endpoint,
            data: {'amount': value, 'from': $('#ex_type').val(), 'to': "DENCH"},
            success: function (data) {
                value1
                    .val(data.amount)
                    .removeClass('loading');
                if(value1.val() !== '0') {
                    $(".buy-btn.trade-button").removeClass('disabled');
                    setBuyDenchButtonURL(data.swap_url)
                }
                else {
                    $(".buy-btn.trade-button").addClass('disabled');
                }
            },
            error: function (error_data) {
                console.log(error_data);
            }
        }).done((e) => {
            buyDenchDiv.css('opacity', 1)
            buyDenchDiv.css('pointer-events', 'unset')
            canDoInput = true
        })
    }
}

function setBuyDenchButtonURL(url) {
    $('.buy-btn.trade-button').attr('href', url)
}