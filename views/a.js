
const Koa = require('koa');
const app = new Koa();
const nunjucks = require('nunjucks');
const templating = require('./templating');


app.use(templating('views', {

    noCache: !isProduction,

    watch: !isProduction

}));

app.use(async ctx => {
  ctx.render('video.html');
});

app.listen(3001);
