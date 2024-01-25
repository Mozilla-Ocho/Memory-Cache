import { io } from "socket.io-client";
import "./styles.css";

const socket = io(`http://${window.location.hostname}:5000`);
socket.on("connect", () => {
  console.log("connected");
});

socket.on("disconnect", () => {
  console.log("disconnected");
});

socket.on("message", (message) => {
  console.log(message);
});

socket.on("error", (error) => {
  console.error(error);
});

// socket.emit("message", JSON.stringify({ text: "hello world!" }));

const chatHistory = document.getElementById("chat-history");
const chatTextArea = document.getElementById("chat-textarea");
const sendButton = document.getElementById("send-button");

function ChatHistoryMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("chat-history-message");
  messageElement.innerText = message;
  return messageElement;
}
let nextChatMessage = ChatHistoryMessage("Hello!");
// chatHistory.appendChild(nextChatMessage);

const replies = new Map();

socket.on("message", (raw) => {
  console.log("Received message from server:", raw);
  const message = JSON.parse(raw);
  console.log("message", message);

  if (message.kind === "first_reply") {
    nextChatMessage = ChatHistoryMessage("");
    chatHistory.appendChild(nextChatMessage);

    replies.set(message.message_sid, {
      first: message,
      chatMessage: nextChatMessage,
    });
    nextChatMessage.innerText += message.text;
  } else if (message.kind === "second_reply") {
    const reply = replies.get(message.message_sid);
    reply.second = message;
    // reply.chatMessage.innerText += "\n";
    // reply.chatMessage.innerText += `\n${message.text}\n`;
    // Send reply and text
    reply.chatMessage.innerText += `\n[Replied in ${message.time} seconds.]\n${message.text}\n`;
  } else if (message.kind === "source_document") {
    const { message_sid, kind, text, source } = message;
    const reply = replies.get(message.message_sid);
    reply.sourceDocuments = reply.sourceDocuments || [];
    reply.sourceDocuments.push(message);
    reply.chatMessage.innerText += `\n\n[${source}]\n${text}\n`;
  }

  // We don't scroll to the bottom while the server is sending us messages.
});

function sendChatMessage() {
  const text = chatTextArea.value;
  chatTextArea.value = "";

  chatHistory.appendChild(ChatHistoryMessage(text));

  // Scroll to the bottom of the chatHistory
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Send the message to the server
  socket.send(
    JSON.stringify({
      text,
    }),
  ); // This will be sent as a JSON string
  console.log("Message sent to server: " + text);
}

let isShiftPressed = false;
chatTextArea.addEventListener("keydown", (event) => {
  if (event.key === "Shift") {
    isShiftPressed = true;
  }
});
chatTextArea.addEventListener("keyup", (event) => {
  if (event.key === "Shift") {
    isShiftPressed = false;
  }
});
chatTextArea.addEventListener("input", (event) => {
  if (event.inputType === "insertLineBreak" && !isShiftPressed) {
    sendChatMessage();
  }
});
sendButton.addEventListener("click", sendChatMessage);
