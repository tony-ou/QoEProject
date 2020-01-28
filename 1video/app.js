const Koa = require('koa');

const bodyParser = require('koa-bodyparser');

const controller = require('./controller');

const templating = require('./templating');

const fs = require('fs');

const rimraf = require("rimraf");

const app = new Koa();

const isProduction = process.env.NODE_ENV === 'production';

var prompt = require('prompt-sync')();

var dummy = true;

//Initialize results
if (fs.existsSync('./results')) {
    var answer = prompt(`results folder already exists. Do you want to overwrite it? (Y/N) `);
    if (answer !== 'Y')
    {
        process.exit();
    }
    rimraf.sync("./results");
}
fs.mkdirSync('./results');



// log request URL:
app.use(async (ctx, next) => {
    console.log(`Process ${ctx.request.method} ${ctx.request.url}...`);
    var
        start = new Date().getTime(),
        execTime;
    await next();
    execTime = new Date().getTime() - start;
    ctx.response.set('X-Response-Time', `${execTime}ms`);
});

// parse user from cookie:
app.use(async (ctx, next) => {
    ctx.state.user = parseUser(ctx.cookies.get('name') || '');
    await next();
});

// static file support:
if (! isProduction) {
    let staticFiles = require('./static-files');
    app.use(staticFiles('/static/', __dirname + '/static'));
}

// parse request body:
app.use(bodyParser());

// add nunjucks as view:
app.use(templating('views', {
    noCache: !isProduction,
    watch: !isProduction
}));

// add controller:
app.use(controller());

app.listen(3001);
console.log('app started at port 3001...');

function parseUser(obj) {
    if (!obj) {
        return;
    }
    //console.log('try parse: ' + obj);
    let s = '';
    if (typeof obj === 'string') {
        s = obj;
    } else if (obj.headers) {
        let cookies = new Cookies(obj, null);
        s = cookies.get('name');
    }
    if (s) {
        try {
            let user = JSON.parse(Buffer.from(s, 'base64').toString());
            //console.log(`User: ${user.mturkID}, ID: ${user.video_order}`);
            return user;
        } catch (e) {
            // ignore
        }
    }
}
