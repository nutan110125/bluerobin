
function headerbg() {

	var scroll = $(window).scrollTop();

	if (scroll >= 100) {
		$("header").addClass("header-bg");
	} else {
		$("header").removeClass("header-bg");
	}
}

$(window).scroll(function () {
	headerbg();
});

$(document).ready(function () {
	$(".filter").click(function () {
		$(this).parents("div.filter-select").next().toggleClass("show");
		/* $(".filter_dropdown").addClass("show"); */
	});
	$(".close_filter").click(function () {
		$(this).parents("div.filter_dropdown").removeClass("show");
	});

	$(".nav-link").click(function () {
		$(".filter_dropdown").removeClass("show");
	});

	$(".custom_tabs li").click(function () {
		var getIndex = $(this).index();
		$(this).parent().parent().parent().find(".lower-filter .custom_filter_job").eq(getIndex).addClass("active").siblings().removeClass("active");
	});

	$(document).on("click", ".head-user-img", function () {
		$(".head-drop-down").toggleClass("show");
		if ($(".notification-drop-down").hasClass("show")) {
			$(".notification-drop-down").toggleClass("show");
		}
	});

	$(document).on("click", ".notification", function () {
		$(".notification-drop-down").toggleClass("show");
		if ($(".head-drop-down").hasClass("show")) {
			$(".head-drop-down").toggleClass("show");
		}
		$.ajax({
			url: '/seen-notification',
			type: "GET",
			dataType: 'json',
			data: {
				"csrfmiddlewaretoken": '{{ csrf_token }}',
			},
			success: function (success) {
				$(".notification-count").text("0")
				console.log("Notification seen Successfully")
			}
		});
	});

	$(document).on("click", ".toggle_search ", function () {
		$(".header_search_box").toggleClass("show");
	});

	$(document).on("click", ".chat_open_btn ", function () {
		$(".chat_left_panel").toggleClass("show");
		$("body").toggleClass("stopscroll");
	});

	$(".dropdownSearchToggle .btn").click(function () {
		$(".dropdownStyleMenu").toggleClass("show");
	});

	$(".dropdownStyleMenu .dropdown-item").click(function () {
		var getVal = $(this).html();
		$(".dropdownSearchToggle input").val(' ');
		$(".dropdownSearchToggle input").val(getVal);
	});


	$(document).click(function (e) {
		if (!$(e.target).is(".dropdownSearchToggle .btn, .dropdownSearchToggle .btn *,.dropdownStyleMenu,.dropdownStyleMenu *")) {
			$('.dropdownStyleMenu').removeClass('show');
		}
	});

	$(".favIcon").click(function () {
		$(this).toggleClass("active");
	});

});





