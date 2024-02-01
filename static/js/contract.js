$("#input_wallet, #input_passcode").change(function () {
    if ($('#input_wallet').val() !== "" && $('#input_passcode').val() !== "") {
        $('.check_btn').removeClass("disabled");
    } else {
        $('.check_btn').addClass("disabled");
        $(".resign_btn").addClass("hidden");
        $(".wrapper_table_check_contract").addClass("hidden");
    }

});


$(".check_btn").on('click', function () {
    let saved_data = null;
    let endpoint = '/api/check_contract';
    $.ajax({
        method: "POST",
        url: endpoint,
        data: {
            'wallet_address': $("#input_wallet").val(),
            'passcode': $("#input_passcode").val()
        },
        success: function (data) {
            let resign_btn = $(".resign_btn");
            resign_btn.removeClass("hidden");
            let wrapper_table_check_contract = $(".wrapper_table_check_contract");
            wrapper_table_check_contract.removeClass("hidden");
            resign_btn.addClass("disabled");
            $(".table_check_contract").remove();
            data['labels'].splice(3, 0, 'current reward')
            let now = new Date();
            let this_mount_start_date = new Date(now.getFullYear(), now.getMonth(), 1)
            let days_this_mount = Math.floor((now - this_mount_start_date) / (1000 * 60 * 60 * 24));
            for (let j = 0; j < data['pairs'].length; j++) {
                let start_time = new Date(data['pairs'][j][data['pairs'][j].length - 1]);
                let calculation_start = 0;
                if (start_time.getMonth() + 1 >= now.getMonth()) {
                    calculation_start = Math.floor((now - start_time) / (1000 * 60 * 60 * 24));
                } else {
                    calculation_start = days_this_mount;
                }

                let coin_count = parseFloat(data['pairs'][j][data['labels'].indexOf('amount_quote') - 1]);
                let percent = parseFloat(data['pairs'][j][data['labels'].indexOf('APR')]);
                let reward = calculation_start * ((coin_count * percent) / 100) / 365;
                data['pairs'][j].splice(3, 0, reward.toFixed(3))
            }
            for (let j = 0; j < data['pairs'].length; j++) {
                let date = new Date(data['pairs'][j][data['pairs'][j].length - 1]);
                data['pairs'][j][data['pairs'][j].length - 1] = date.toLocaleString()
            }
            for (let j = 0; j < data['labels'].length; j++) {
                data['labels'][j] = data['labels'][j].replace('_', ' ');
                if (data['labels'][j] === 'timestamp') {
                    data['labels'][j] = 'date time'

                }
            }

            if (data['pairs'].length !== 0) {
                let table = makeTable(data['labels'], data['pairs']);
                saved_data = data['pairs'];
                $(table).insertAfter($('.insert_table'));
                $('input[type="checkbox"]').on('change', function () {
                    $('input[name="' + this.name + '"]').not(this).prop('checked', false);
                    console.log(this.checked);
                    if (this.checked) {
                        $(".resign_btn").removeClass("disabled");
                    } else {
                        $(".resign_btn").addClass("disabled");
                    }
                });
            } else {
                resign_btn.addClass("hidden");
                wrapper_table_check_contract.addClass("hidden");
                resign_btn.removeClass("disabled");
            }
        },
        error: function (error_data) {
            console.log(error_data);
        },
    });
    $(".resign_btn").on('click', function () {
        $(".check_btn").addClass('disabled');
        $("#wallet-hash-resign, #countdown-timer-resign, #wallet-hash-wrapper-resign").remove();
        $('#confirm-resign-btn').remove();
        $('#massage').remove()
        let checked_index = parseInt($('input[name="table_connected_group"]:checked').val());
        let TokenLP_value = saved_data[checked_index][6];

        let hash = "<div id='wallet-hash-wrapper-resign' class='wallet-hash-wrapper1'><span id='wallet-hash-resign' class='wallet-hash1' title='Click to copy'>0xa1e453b2c576acEEA6d406b7366536feB8A6DF55</span></div>";
        $("<div class='send-confirm-btn' id='confirm-resign-btn'><span style='color: #212529'>CONFIRM</span></div>").insertAfter($(this));
        $("<div id = 'massage' style='color: #ffc955'><br><h5 id='massage_text'>Send us back TokenLP: " + TokenLP_value + " </h5></div>").insertBefore($(this));
        $(this).addClass('hidden');
        $('#wallet-hash-wrapper-resign').on('click', function () {
            copyToClipboard($(this).text());
        });
        $("#wrapper_table_check_contract_id").addClass('hidden');
        $('<p id="countdown-timer-resign" class="countdown-timer1">4 m 59 s</p>' + hash).insertBefore($(this));
        let countDownDate = new Date().getTime() + 300000;
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
            if ($("#countdown-timer-resign").length < 1) {
                clearInterval(x);
                return;
            }
            let string = document.getElementById("countdown-timer-resign").innerHTML;
            if (string.includes('m ')) {
                document.getElementById("countdown-timer-resign").innerHTML = minutes + "m " + seconds + "s";
            }

            // If the count down is over, write some text
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("countdown-timer-resign").innerHTML = "EXPIRED";
                setTimeout(function () {
                    $("#wallet-hash-resign, #countdown-timer-resign, #wallet-hash-wrapper-resign").remove();
                    $('.resign_btn').addClass("hidden");
                    $('#confirm-resign-btn').remove();
                    $(".check_btn").removeClass('disabled');
                    $('#massage').remove()

                }, 1500);
            }
        }, 1000);


        $("#confirm-resign-btn").on('click', function () {
            $("#wallet-hash-resign, #wallet-hash-wrapper-resign").remove();
            $("#confirm-resign-btn").remove();
            let endpoint = '/api/resign_contract';
            $.ajax({
                method: "POST",
                url: endpoint,
                data: {
                    'wallet_address': $("#input_wallet").val(),
                    'passcode': $("#input_passcode").val(),
                    'index': $('input[name="table_connected_group"]:checked').val()
                },
                success: function (data) {
                    document.getElementById("countdown-timer-resign").innerHTML = data.response;
                    setTimeout(function () {
                        $("#countdown-timer-resign").remove();
                        $('#confirm-resign-btn').remove();
                        $(".check_btn").removeClass('disabled');
                        $('#massage').remove()
                    }, 10000);
                },
                error: function (error_data) {
                    console.log(error_data);
                },
            });
        });
    });
});

function makeTable(header, array) {
    let table = document.createElement('table');
    $(table).addClass("table_check_contract")
    let header_row = document.createElement('tr');
    let header_element = document.createElement('th');
    header_element.textContent = "  ";
    header_row.appendChild(header_element);
    for (let h = 0; h < header.length; h++) {
        let header_element = document.createElement('th');
        header_element.textContent = header[h];
        header_row.appendChild(header_element);
    }
    table.appendChild(header_row);
    for (let i = 0; i < array.length; i++) {
        let coin_names = ['BUSD', 'DENCH', 'DODO', 'BNB', 'ETH']
        let row = document.createElement('tr');
        let cell = document.createElement('td');
        let input = document.createElement('input');
        input.type = 'checkbox';
        input.name = 'table_connected_group';
        input.value = i.toString();
        cell.appendChild(input);

        row.appendChild(cell);
        for (let j = 0; j < array[i].length; j++) {
            let cell = document.createElement('td');
            if (coin_names.includes(array[i][j])) {

                let img = document.createElement('img');
                img.alt = "logo";
                $(img).addClass("logos");
                img.src = "/static/images/" + array[i][j].toLowerCase() + "-logo.png";
                cell.appendChild(img);
                let span = document.createElement('span');
                span.textContent = array[i][j];
                cell.appendChild(span);
            } else {
                cell.textContent = array[i][j];
            }
            row.appendChild(cell);
        }
        $(row).addClass("checkbox_row")
        $(row).addClass(i.toString())
        table.appendChild(row);
    }
    return table;
}

function copyToClipboard(text) {
    let sampleTextarea = document.createElement("textarea");
    document.body.appendChild(sampleTextarea);
    sampleTextarea.value = text; //save main text in it
    sampleTextarea.select(); //select textarea contents
    document.execCommand("copy");
    document.body.removeChild(sampleTextarea);
}

$.fn.contracts = function (options) {
    const container = $(this);
    return options.forEach(option => {
        const element = $($.parseHTML(`
            <div class="send-dench_newline">
                <h5 class="contract_first">
                    <img class="logos src-logo" alt="logo"/> <span class="src-title"></span> -
                    <img class="logos dst-logo" alt="logo"/> <span class="dst-title"></span>
                </h5>
                <br>
                <br>
                <h6 class="contract_second">
                    APR: <span class="apr-value" data-apr="${option.apr}"></span>
                    <br>
                    REWARD: <span class="reward-value"></span>
                </h6>
                <br>
                <br>
                <input type="number" min="0" placeholder="0.000" class="reward-input reward hidden"
                       oninput="this.value = Math.abs(this.value)"/>
                <div class="send-btn hidden">
                    <span style="color: #212529">${option.translations.SEND}</span>
                </div>
                <h6 class="contract_calculator hidden">
                    Send us <br> <span class="src-title"></span>: <input class="src-count-input coin_count" placeholder="0" disabled/>
                    <br> <span class="dst-title"></span>: <input class="dst-count-input coin_count" placeholder="0" disabled/></h6>
                <div class="activate-btn">
                    <span style="color: #212529">${option.translations.ACTIVATE}</span>
                </div>
            </div>`));

        element.find('.src-title').text(option.source);
        element.find('.dst-title').text(option.destination);

        element.find('.apr-value').text(option.apr + '%');
        element.find('.reward-value').text(option.destination);

        element.find('.src-logo').attr('src', option.sourceLogo);
        element.find('.dst-logo').attr('src', option.destinationLogo);

        const sendBtn = element.find('.send-btn');
        const activateBtn = element.find('.activate-btn');
        const rewardInput = element.find('.reward-input');
        const srcCountInput = element.find('.src-count-input');
        const dstCountInput = element.find('.dst-count-input');
        const contractcalculator = element.find('.contract_calculator');
        const aprvalue = element.find('.apr-value').data('apr');
        let sendconfirmBtn = element.find('.send-confirm-btn');

        activateBtn.on('click', function () {
            element.find('.hidden').removeClass('hidden');
            activateBtn.addClass('hidden');
            sendBtn.addClass("disabled");
            let hash = "<div class='wallet-hash-wrapper1'><span class='wallet-hash1' title='Click to copy'>0xa1e453b2c576acEEA6d406b7366536feB8A6DF55</span></div>";
            $('<p class="countdown-timer1">4 m 59 s</p>' + hash).insertBefore($(this));
            let countdowntimer = element.find('.countdown-timer1');
            let wallethashwrapper = element.find('.wallet-hash-wrapper1');
            let wallethash = element.find('.wallet-hash1');
            wallethashwrapper.on('click', function () {
                copyToClipboard($(this).text());
            });
            // Set the date we're counting down to
            let countDownDate = new Date().getTime() + 300000;
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
                if (countdowntimer.length < 1) {
                    clearInterval(x);
                    return;
                }
                let string = countdowntimer.text();
                if (string.includes('m ')) {
                    countdowntimer.text(minutes + "m " + seconds + "s");
                }

                // If the count down is over, write some text
                if (distance < 0) {
                    clearInterval(x);
                    countdowntimer.text("EXPIRED");
                    setTimeout(function () {
                        wallethash.remove();
                        wallethashwrapper.remove();
                        activate_contract_back();
                    }, 1500);
                }
            }, 1000);

            function activate_contract_back() {
                countdowntimer.remove();
                activateBtn.removeClass("hidden");
                contractcalculator.addClass("hidden");
                rewardInput.prop('disabled', false);
                rewardInput.addClass("hidden");
                sendconfirmBtn.remove();
                sendBtn.show();
                sendBtn.addClass("hidden");
            }

            rewardInput.change(function () {
                let endpoint = '/api/calculate_coin_amount';
                if ($(this).val() !== '') {
                    let a = $(this).val();
                    srcCountInput.val(a)
                    dstCountInput.addClass("loading");
                    $.ajax({
                        method: "POST",
                        url: endpoint,
                        data: {'amount': a, 'from': option.source, 'to': option.destination},
                        success: function (data) {
                            dstCountInput
                                .val(data.amount)
                                .removeClass("loading");
                            if (dstCountInput.val() !== '0') {
                                sendBtn.removeClass("disabled")
                            }
                            else {
                                sendBtn.addClass('disabled');
                            }
                        },
                        error: function (error_data) {
                            console.log(error_data);
                        }
                    })
                }
            });

            sendBtn.on('click', function () {
                sendconfirmBtn.remove();
                let hash = "<div class='send-confirm-btn'><span style='color: #212529'>CONFIRM</span></div>"
                let that = $(this);
                $(hash).insertBefore($(this));
                sendconfirmBtn = that.parent().find('.send-confirm-btn');
                $(this).hide();
                rewardInput.prop('disabled', true);
                sendconfirmBtn.on('click', function () {
                    wallethash.remove();
                    wallethashwrapper.remove();
                    sendconfirmBtn.addClass('disabled');
                    let endpoint = '/api/paired_transaction';
                    $.ajax({
                        method: "POST",
                        url: endpoint,
                        data: {
                            'base': option.source,
                            'quote': option.destination,
                            'base_amount': srcCountInput.val(),
                            'quote_amount': dstCountInput.val(),
                            'apr': aprvalue,
                            'chain_type': option.chain_type,
                        },
                        success: function (data) {
                            let response = data.response;
                            countdowntimer.text(" ");
                            if (response.includes('Success') && response.includes('passcode')) {
                                let splited = response.split(" : ");
                                let span = document.createElement('span');
                                span.textContent = splited[0];
                                countdowntimer.append(span);
                                let span1 = document.createElement('span');
                                span1.title = 'Click to copy';
                                span1.classList.add("wallet_passcode");
                                span1.id = "wallet_passcode_item";
                                span1.textContent = splited[1];
                                countdowntimer.append(span1);
                                const walletPasscode = element.find('.wallet_passcode');
                                walletPasscode.on('click', function () {
                                    copyToClipboard($(this).text());
                                    setTimeout(activate_contract_back, 1000);
                                });
                            } else {
                                countdowntimer.text(response);
                                setTimeout(activate_contract_back, 2000);
                            }
                        },
                        error: function (error_data) {
                            console.log(error_data);
                        },
                    });
                });
            });

        });
        container.append(element);
    });
};



