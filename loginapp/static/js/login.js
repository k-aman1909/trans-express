$(function () {
	$('input[type="text"],input[type="password"]').keypress(function (e) {
		if (e.which == 32) {
			if (e.target.selectionStart === 0) return false;
			else if ($(this).val().slice(-1) === " ") e.preventDefault();
		} else {
			// alert('ok')
			$(this).siblings("span").html("");
		}
	});
	$('input[type="text"], input[type="password"]').keyup(function (e) {
		if (e.which == 8) {
			$(this).siblings("span").html("");
		}
	});
	$('input[type="text"]').focusout(function (e) {
		if ($(this).val().length == 0) {
			$(this).siblings("span").html("This Field is Mandatory!");
		}

	});
	$('input[type="text"]').focusin(function (e) {
		if ($(this).val() == "This is mandatory*") {
			$(this).val("");
		}
		$(this).css({ color: "black" });
	});
});
function number(no) {
	$(no).keypress(function (e) {
		var len = $(this).val().length;
		if (len == 10) {
			$(no).siblings("span").html("Maximum 10 digits are allowed").css({ color: "red" });
			e.preventDefault();
		} else if (!(e.which >= 48 && e.which <= 57)) {
			$(no).siblings("span").html("Only Digits are Allowed").css({ color: "red" });
			e.preventDefault();
		} else if (e.which == 48) {
			if (e.target.selectionStart === 0) return false;
		} else {
			$(no).siblings("span").html("");
		}
	});
	$(no).focusout(function (e) {
		var len = $(this).val().length;
		if (len < 10) {
			$(no).siblings("span").html("Minimum 10 digits are required").css({ color: "red" });
		} else if (len == 10) {
			$(this).siblings("span").html("");
		} else if (
			len == 0 &&
			$(this).siblings("span").html("") == "Only Digits are Allowed"
		) {
			$(this).siblings("span").html("");
		} else if ($(this).val() == "") {
			$(this).val("This is mandatory*");
			$(this).siblings("span").html("");
			e.preventDefault();
		}
	});
}
function alphabets(name) {
	$(name).keypress(function (e) {
		if (
			!(
				(e.which >= 65 && e.which <= 90) ||
				(e.which >= 97 && e.which <= 122) ||
				e.which == 32 ||
				e.which == 46
			)
		) {
			$(name)
				.siblings("span")
				.html("Only Alphabets are Allowed")
				.css({ color: "red" });
			return false;
		} else if (e.which == 46) {
			if (e.target.selectionStart === 0) return false;
			else if ($(this).val().slice(-1) === ".") e.preventDefault();
		} else {
			$(name).siblings("span").html("");
		}
	});
}