$('#sort-selector').change(function () {
    const selector = $(this);
    const thisUrl = new URL(window.location);
    const order = selector.val();
    if (order != "reset") {
        const sort = order.split("_")[0];
        const direction = order.split("_")[1];
        thisUrl.searchParams.set("sort", sort);
        thisUrl.searchParams.set("direction", direction);
        window.location.replace(thisUrl);
    } else {
        thisUrl.searchParams.delete("sort");
        thisUrl.searchParams.delete("direction");
        window.location.replace(thisUrl);
    }
})