window.addEvent('domready', function () {
    $$('input').set({
        events: {
            change: function (el) {
                $$('label').removeClass('selected');
                this.getParent('label').addClass('selected');
            }
        }
    });
});
