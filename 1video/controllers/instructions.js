

module.exports = {
	
    'GET /': async (ctx, next) => {
        ctx.render('instructions.html', {
            title: 'Welcome'
        });
    }
};
