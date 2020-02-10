// start test:
var getOder = require('../models/random');
var fs = require('fs');

const vid_folder = "2vid_test";
var vid_path = "../videos/" + vid_folder;
var video_url = "https://github.com/tony-ou/QoEProject/raw/master/videos/" + vid_folder + "/";

var num_vids;

fs.readdir(vid_path, function(err, files) {
    num_vids = files.length / 2;
    console.log(vid_path + " has " + num_vids + " files");
});

var post_start = async (ctx, next) => {
    var mturkID = ctx.request.body.MTurkID;
    var device = ctx.request.body.device;
    var age = ctx.request.body.age;
    var network = ctx.request.body.network;
    var video_order = getOder(1,num_vids);
    console.log(mturkID, device, age);
    var start = new Date().getTime();

    let user = {
        mturkID : mturkID,
        device : device,
        age : age,
        network : network,
        video_order : video_order,
        count : 1,
        lResult : [],
        rResult : [],        
        video_time : [],
        grade_time : [],
        start : start
    };
    var i;
    //initialize video_time & grade_time
    for (i = 0; i < num_vids; i++)
    {
    	user.video_time.push(0);
    	user.grade_time.push(0);
    }
    
    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    ctx.cookies.set('name', value);
    var l_video_src = video_url + video_order[0] + "_0.mp4";
    var r_video_src = video_url + video_order[0] + "_1.mp4";
    
    // https://github.com/michaelliao/learn-javascript/raw/master/video/vscode-nodejs.mp4
    // very interesting url!

    var title = "1/" + num_vids;

    ctx.render('video.html', {
        title: title, l_video_src : l_video_src, r_video_src : r_video_src,  count: user.count, num_vids: num_vids
    });
}




var post_next = async (ctx, next) => {
    var user = ctx.state.user;
    var lGrade = ctx.request.body.lSentiment;
    var rGrade = ctx.request.body.rSentiment;
    user.lResult.push(lGrade);
    user.rResult.push(rGrade);
   	//console.log(ctx.request.body.lClicktime)
   	//console.log(ctx.request.body.rClicktime)

    var end = new Date().getTime();
    var exe_time = end - user.start;
    user.video_time[user.count-1] += exe_time;

    user.start = end;
    if(user.count < num_vids) {
        var video_src = video_url + user.video_order[user.count] + ".mp4";
        user.count = user.count + 1;
        var title = user.count + "/" + num_vids;

        // set new cookie
        let value =  Buffer.from(JSON.stringify(user)).toString('base64');
        ctx.cookies.set('name', value);
        ctx.render('video.html', {
            title: title, video_src: video_src, count: user.count, num_vids: num_vids
        });
    }
    else {
         // set new cookie
        let value =  Buffer.from(JSON.stringify(user)).toString('base64');
        ctx.cookies.set('name', value);
        ctx.render('reason.html', {
            title: 'Post Survey Question'
        });
    }
}

var post_end = async (ctx, next) => {
    var user = ctx.state.user;
    
    // set user reason
    var reason = ctx.request.body.Reason;
    console.log("reason is " + reason + "\n");
    user.reason = reason;

    // record results
    console.log(user.result);
    var filename = "./results/" + user.mturkID + ".txt";
    var write_data = [];
    var write_video_time = [], write_grade_time =[];
    for(var i in user.video_order) {
        write_data[user.video_order[i] - 1] = [user.lResult[i].toString() + " "+user.rResult[i].toString()];
        write_video_time[user.video_order[i] - 1] = user.video_time[i];
    }
    fs.writeFile(filename, write_data + '\n'+ user.video_order + '\n' + 
                write_video_time + '\n'
                 + write_grade_time + '\n' + user.mturkID + '\n' 
                 + user.device + '\n' + user.age + '\n' 
                 + user.network + '\n' + user.reason, function(err) {
        if(err) {
            return console.log(err);
        }
    });
    // clear cookie
    ctx.cookies.set('name','');
    
    var return_code = "0lMq2GKqLDSUgYAGc=";
    ctx.render('ending.html', {
        title: 'Thank you', return_code:return_code
    });
}
                 

module.exports = {
    'POST /start' : post_start,
    'POST /next' : post_next,
    'POST /end' : post_end
};
