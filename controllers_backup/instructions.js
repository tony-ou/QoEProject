

module.exports = {
	
    'GET /': async (ctx, next) => {
    	    ctx.render('video.html', {
        title: 'gg', video_src : ''
    });
/*
        ctx.render('instructions.html', {
            title: 'Welcome'
        });
*/
    }
};
