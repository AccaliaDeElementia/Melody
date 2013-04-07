/*jslint browser: true, maxlen: 79 */
/*globals io: true, jQuery: true */
(function($) {
    'use strict';
    /* jQuery Tiny Pub/Sub - v0.7 - 10/27/2011
     * http://benalman.com/
     * Copyright (c) 2011 "Cowboy" Ben Alman; Licensed MIT, GPL */
    var o = $({});

    $.subscribe = function() {
        o.on.apply(o, arguments);
    };

    $.unsubscribe = function() {
        o.off.apply(o, arguments);
    };

    $.publish = function() {
        o.trigger.apply(o, arguments);
    };
}(jQuery));

(function($, window) {
    'use strict';
    var socket, Melody, rStrip = /^\s+|\s+$/g;
    function setRating(data) {
        var rating = data.message;
        if (data.code === 200) { rating = data.extra.Rating; }
        console.log(rating);
        if (!rating) { return; }
        rating.split(' ').forEach(function(item) {
            if (!item) { return; }
            var cfg = [['good', '.piano-rate-up'], ['bad', '.piano-rate-down'],
                ['seed', '.piano-song-seed'],
                ['artistseed', '.piano-artist-seed']];
            cfg.forEach(function(config) {
                if (item === config[0]) {
                    $(config[1]).addClass('ui-state-highlight');
                } else {
                    $(config[1]).removeClass('ui-state-highlight');
                }
            });
        });
    }

    Melody = {
        start: function() {
            this.connect();
            this.register_updates();
            this.register_controls();
            this.login();
        },
        connect: function() {
            socket = io.connect('ws://' + location.host + ':4446');
            socket.on('stream', function(data) {
                $.publish('piano-*', data.message);
                $.publish('piano-' + data.code, data.message);
            }).on('response', function(data) {
                $.publish('piano-command-' + data.nonce, data);
            }).on('error', function(data) {
                $.publish('piano-error', data);
            });
        },
        register_updates: function() {
            $('.piano-update').each(function() {
                var key, attr, fn, jthis;
                jthis = $(this);
                this.className.split(' ').forEach(function(item) {
                    if (item.indexOf('piano-key-') === 0) {
                        key = item.replace('key-', '');
                    }
                    if (item.indexOf('piano-attr-') === 0) {
                        attr = item.replace('piano-attr-', '');
                    }
                });
                if (attr) {
                    fn = function(evt, data) {
                        jthis.attr(attr, data.message);
                    };
                } else {
                    fn = function(evt, data) {
                        jthis.text(data.message);
                    };
                }
                $.subscribe(key, fn);
            });
            $.subscribe('piano-109', function(evt, data) {
                $('.piano-station').text(data.message.replace(/^\S+\s+/, ''));
            });
            $.subscribe('piano-116', function (evt, data) {
                setRating(data);
            });
            [101, 102, 103, 104, 106].forEach(function(item) {
                $.subscribe('piano-' + item, function(evt, data) {
                    $('.piano-status').text(data.name);
                });
            });
        },
        register_controls: function() {
            var self = this, cfg;
            self.execute('stations', function(data) {
                $('.piano-stations option').remove();
                $('.piano-stations').append(
                    '<option value="mix">QuickMix</option>'
                );
                data.message.Station.forEach(function(item) {
                    $('.piano-stations').append(
                        '<option value="' + item + '">' + item
                            + '</option>'
                    );
                });
                $('.piano-stations').val($('.piano-station').text());
            });
            $('.piano-set-station').click(function() {
                var station = $('.piano-stations').val(),
                    command = 'SELECT MIX';
                if (station !== 'mix') {
                    command = 'SELECT STATION "' + station + '"';
                }
                self.execute(command);
            });
            $('.piano-play').click(function() { self.execute('PLAYPAUSE'); });
            $('.piano-stop').click(function() { self.execute('STOP'); });
            $('.piano-skip').click(function() { self.execute('SKIP'); });

            cfg = [['.piano-rate-down', 'BAD'], ['.piano-rate-up', 'GOOD'],
                ['.piano-ban', 'OVERPLAYED']];
            cfg.forEach(function(config) {
                $(config[0]).click(function() {
                    var id = $('.piano-key-111').attr('id'),
                        active = $(config[0]).hasClass('ui-state-highlight');
                    if (active) {
                        self.execute('RATE NEUTRAL "' + id + '"', setRating);
                    } else {
                        self.execute('RATE ' + config[1] + ' "' + id + '"',
                            setRating);
                    }
                });
            });
            $('.piano-controls div').hover(function() {
                $(this).addClass('ui-state-hover');
            }, function() {
                $(this).removeClass('ui-state-hover');
            });
        },
        execute: function(command, callback) {
            var login = 'USER "%USER%" "%PASS%"\n',
                username = $('.piano-username').val(),
                password = $('.piano-password').val(),
                nonce = (new Date()).getTime(),
                key = 'piano-command-' + nonce,
                oncomplete;
            login = login.replace('%USER%', username);
            login = login.replace('%PASS%', password);
            if (username && password) {
                login += command;
            } else {
                login = command;
            }
            login = login.replace(rStrip, '');
            oncomplete = function(evt, data) {
                $.unsubscribe(key, oncomplete);
                if (callback && callback.call) {
                    callback(data);
                }
            };
            $.subscribe(key, oncomplete);
            socket.emit('command', {
                text: login,
                nonce: nonce
            });
        },
        login: function() {
            var username = $('.piano-username'),
                password = $('.piano-password');
            if (!username.val()) {
                username.val($.cookie('piano-username'));
            }
            if (!password.val()) {
                password.val($.cookie('piano-password'));
            }
            $.cookie('piano-username', username.val(), {expires: 365});
            $.cookie('piano-password', password.val(), {expires: 365});
            if (!username.val() || !password.val()) { return; }
            this.execute('', function(data) {
                if (data.code === 200) {
                    $('.piano-login-error').hide();
                    $('.piano-login-container').hide();
                    $('.piano-controls').show();
                    $.publish('piano-login', true);
                } else {
                    $('.piano-login-error').text(data.message).show();
                    $('.piano-login-container').show();
                    $('.piano-controls').hide();
                    $.publish('piano-login', false);
                }
            });
        }
    };
    window.Melody = Melody;
}(jQuery, window));
