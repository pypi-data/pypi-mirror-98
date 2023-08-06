$(document).ready(function () {
    'use strict';

    /**
     * extend links to external website
     * » add target="_blank"
     * » add rel="noopener noreferer"
     */
    let externalLinks = function () {
        // let internalHost = location.hostname.replace(/ /g, '').split(',');
        let internalHost = [location.hostname];
        let protocolPattern = /^https?:\/\//i;

        /**
         * walk through all links on the current page
         */
        $('a').each(function () {
            let href = $(this).attr('href');

            /**
             * check if its a http link
             */
            if (protocolPattern.test(href)) {
                let hrefHostname = $(new URL(href)).attr('hostname');

                if ($.inArray(hrefHostname, internalHost) === -1) {
                    $(this).attr('target', '_blank');
                    $(this).attr('rel', 'noopener noreferer');
                }
            }
        });
    };

    /**
     * functions that need to be executed on load
     */
    let init = function () {
        externalLinks();
    };

    /**
     * start the show
     */
    init();

    /**
     * functions that need to be executed on successful ajax events
     */
    $(document).ajaxSuccess(function() {
        externalLinks();
    });
});
