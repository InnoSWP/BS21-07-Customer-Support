const express = require('express');
var cors = require('cors');
const app = express();
app.use(cors());

const TelegramBot = require('node-telegram-bot-api');

const port = 3001;
const telegram_token = "5505131588:AAF_LojeoLfIAlhd6UJnV36gDS-yDZei9Nw";
const chatId = 404548645;

const bot = new TelegramBot(telegram_token, {polling: true});

bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "Your id" + chatId);
    console.log(chatId);
    //bot.sendMessage(chatId, "HO HO HO");
});

app.get('/', function (req, res) {
    console.log();
    var msg = req.query.message !== undefined ? req.query.message : "none";
    msg.trim();
    if(msg) bot.sendMessage(chatId, msg);
    res.send('Service enable');
});
app.get('/getChatId', function (req, res) {
    res.json({chatId});
});

app.listen(port);

console.log("SERVER STARTED ON PORT: " + port);