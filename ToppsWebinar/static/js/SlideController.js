$(function () {
    var localData;
    var currentStep;
    var email = "";
    var jsplayer = videojs('slide-video');
    var maxSteps = 191;

    //localStorage.clear();
    if (localStorage.getItem("topps_data") == undefined || JSON.parse(localStorage.getItem("topps_data")).email != email) {
        localStorage.setItem("topps_data", JSON.stringify({ email: email, step: 1, quizStep: 1 }));
    }

    localData = JSON.parse(localStorage.getItem("topps_data"));
    currentStep = localData.step-1;
    //console.log('Step:', localData.step);
    //console.log('Quiz Step:', localData.quizStep);

    //Add video links
    for (var i = 1; i <= maxSteps; i++) {
        var id;
        if (i < 10) {
            id = '00' + i;
        } else if (i < 100) {
            id = '0' + i;
        } else {
            id = i;
        }

        var classes = (i <= localData.step) ? 'slide-link slide-complete' : 'slide-link';
        classes = (i == 1) ? classes + ' active-link' : classes;
        var html = "<p class='" + classes + "' cid='" + i + "' vid='" + id + "'>Slide " + id;
        html += (i < localData.step) ? " <span class='float-right'>✔</span></p>" : " <span class='float-right'>⨯</span></p>";
        $('#slide-links').append(html);
    }

    //Add completion link
    $('#slide-links').append("<p class='complete-link'>Complete<span class='float-right'>✔</span></p>");
    $('.slide-complete-container').hide();

    jsplayer.on('ended', function () {
        var curlink = $(".slide-link[cid='" + currentStep + "']");
        if (currentStep == 2) {

        }
        if (currentStep < maxSteps) {
            var nexlink = $(".slide-link[cid='" + (currentStep + 1) + "']");
            $('.active-link').removeClass('active-link');
            nexlink.addClass('slide-complete active-link');
            jsplayer.src({ type: "video/mp4", src: 'https://toppscerttest.blob.core.windows.net/videos/' + nexlink.attr('vid') + '.mp4' });
        } else {
            $('.active-link').removeClass('active-link');
            location.href = "../wbwatched";
        }
        curlink.find('.float-right').html('✔');
        currentStep++;
        if (currentStep >= localData.step) {
            localStorage.setItem("topps_data", JSON.stringify({ email: email, step: currentStep, quizStep: localData.quizStep }));
        }
    });

    $('.slide-link').click(function (event) {
        var link = $(event.currentTarget);
        currentStep = parseInt(link.attr('cid'));
        $('.active-link').removeClass('active-link');
        $('.quiz-active-link').removeClass('quiz-active-link');
        link.addClass('active-link');
        jsplayer.src({ type: "video/mp4", src: 'https://toppscerttest.blob.core.windows.net/videos/' + link.attr('vid') + '.mp4' });
        $('.slide-quiz-container').hide();
        $('.slide-video-container').show();
        $('.slide-complete-container').hide();
    });

    $('.complete-link').click(function (event) {
        jsplayer.pause();
        currentQuizStep = maxQuizSteps + 1;
        $('.complete-link').show();
        $('.slide-complete-container').show();
        $('.slide-quiz-container').hide();
        $('.slide-video-container').hide();
        $('.quiz-active-link').removeClass('quiz-active-link');
    });

    $('.review-submit').click(function () {
        jsplayer.pause();
        currentQuizStep = 1;
        $('.active-link').removeClass('active-link');
        $('.quiz-active-link').removeClass('quiz-active-link');
        $(".quiz-link[cid='" + currentQuizStep + "']").addClass('quiz-active-link');
        $('.slide-quiz').hide();
        $(".slide-quiz[cid='" + currentQuizStep + "']").show();
        $('.slide-quiz-container').show();
        $('.slide-video-container').hide();
        $('.slide-complete-container').hide();
    });

    $('.print-submit').click(function () {
        window.open("/Account/Results");
    });

    $('.close-submit').click(function (event) {
        $('.background-shield').hide();
        $('.incorrect').hide();
        $('.correct').hide();
    });
});