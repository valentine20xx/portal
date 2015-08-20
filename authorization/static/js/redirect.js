window.onload = function () {
    setTimeout(function () {
        var urlParams = null;
        (function () {
            var match,
                pl = /\+/g,
                search = /([^&=]+)=?([^&]*)/g,
                decode = function (s) {
                    return decodeURIComponent(s.replace(pl, " "));
                },
                query = window.location.search.substring(1);

            urlParams = {};
            while (match = search.exec(query))
                urlParams[decode(match[1])] = decode(match[2]);
        })();

        if (typeof urlParams.next != "undefined") {
            window.location = urlParams.next
        }
    }, 1000);
}