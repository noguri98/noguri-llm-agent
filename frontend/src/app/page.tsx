"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! How can I help you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new message
  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector(
        "[data-radix-scroll-area-viewport]"
      );
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage.content }),
      });

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      // Temporary assistant message placeholder
      const assistantId = (Date.now() + 1).toString();
      setMessages((prev) => [
        ...prev,
        {
          id: assistantId,
          role: "assistant",
          content: "",
        },
      ]);

      let assistantContent = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6); // Remove "data: " prefix
            if (data === "[DONE]") {
              break;
            }

            // Parse JSON data if needed, or treat as raw text depending on server output
            // Server code: yield {"data": chunk} -> sse-starlette sends data: chunk\n\n
            // So data variable has the chunk content directly.

            assistantContent += data;

            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantId
                  ? { ...msg, content: assistantContent }
                  : msg
              )
            );
          }
        }
      }

    } catch (error) {
      console.error("Error communicating with backend:", error);
      // Optional: Add error message to chat
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-slate-50 p-4 dark:bg-slate-900">
      <Card className="w-full max-w-2xl h-[80vh] flex flex-col shadow-xl">
        <CardHeader className="border-b bg-white dark:bg-slate-950 rounded-t-xl">
          <CardTitle className="flex items-center gap-2">
            <Bot className="w-6 h-6 text-primary" />
            AI Assistant
          </CardTitle>
        </CardHeader>

        <CardContent className="flex-1 p-0 overflow-hidden bg-slate-50/50 dark:bg-slate-900/50">
          <ScrollArea ref={scrollRef} className="h-full p-4">
            <div className="flex flex-col gap-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : "flex-row"
                    }`}
                >
                  <Avatar className="w-8 h-8 border">
                    <AvatarFallback>
                      {message.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                    </AvatarFallback>
                    {message.role === "assistant" && <AvatarImage src="/bot-avatar.png" />}
                  </Avatar>

                  <div
                    className={`rounded-lg px-4 py-2 max-w-[80%] text-sm ${message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-white border text-foreground shadow-sm dark:bg-slate-950"
                      }`}
                  >
                    {message.content}
                    {message.role === "assistant" && message.content === "" && isLoading && (
                      <span className="animate-pulse">...</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>

        <CardFooter className="p-4 border-t bg-white dark:bg-slate-950 rounded-b-xl">
          <div className="flex w-full items-center space-x-2">
            <Input
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1"
              disabled={isLoading}
            />
            <Button size="icon" onClick={handleSend} disabled={!input.trim() || isLoading}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
