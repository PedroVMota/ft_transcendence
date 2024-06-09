import { useEffect, useState } from "react";

interface Error {
    message: string;
}


function NotificationComponent({ data }: { data: Error }) {
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsVisible(false);
        }, 1000);

        return () => clearTimeout(timer); // This will clear the timer when the component unmounts
    }, []);

    if (!isVisible) return null;

    console.log(">>>>>>>>>", data);
    return (
        <div className="absolute top-0 right-0 bg-red-500 text-white p-2 z-10">
            <strong className="font-bold">Error!</strong>
            <span className="block sm:inline">{data.message}</span>
        </div>
    );
}





export function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<Error | null>(null);
    const url = "http://localhost:8000/token/login/"

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const data = { username, password };
        console.log(data);
        try {
            const response = await fetch(url, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                console.log(response);
                const errorData = await response.json();
                setError(errorData);
            }
        } catch (err) {
            if (err instanceof Error) {
                setError({ message: err.message });
            } else {
                setError({ message: 'An unknown error occurred.' });
            }
        }
    }




    return (
        <>
            {error && <NotificationComponent key={error.message} data={error} />}
            <div className="min-h-1/2 flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-md w-full space-y-8">
                    <div>
                        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Login</h2>
                    </div>
                    <form className="mt-8 space-y-6" onSubmit={handleSubmit} method="POST" action="">
                        <div className="rounded-md shadow-sm -space-y-px">
                            <div>
                                <label htmlFor="username" className="sr-only">Username</label>
                                <input id="username" autoComplete="username" name="username" type="text" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Username" onChange={e => setUsername(e.target.value)} />
                            </div>
                            <div>
                                <label htmlFor="password" className="sr-only">Password</label>
                                <input autoComplete="current-password" id="password" name="password" type="password" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password" onChange={e => setPassword(e.target.value)} />
                            </div>
                        </div>

                        <div>
                            <button type="submit" className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Submit
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}
function Comunicate({ WebSocket }: { WebSocket: WebSocket | null }) {
    const [input, setInput] = useState("");
    const [user, setUser] = useState("");
    const [messages, setMessages] = useState<string[]>([]);

    const sendMessage = () => {
        if (WebSocket) {
            WebSocket.send(JSON.stringify({ user, message: input }));
        }
        setInput("");
    };

    useEffect(() => {
        if (WebSocket) {
            WebSocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                setMessages((messages) => [...messages, `${message.user}: ${message.message}`]);
            };
        }
    }, [WebSocket]);

    if (!WebSocket) return (<div>WebSocket not connected</div>);

    return (
        <>
            <input type="text" value={user} onChange={(e) => setUser(e.target.value)} placeholder="Enter your username" />
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Enter your message" />
            <button onClick={sendMessage}>Send</button>
            <div>
                {messages.map((message, index) => (
                    <p key={index}>{message}</p>
                ))}
            </div>
        </>
    );
}




export function Socket() {
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [feedBack, setFeedBack] = useState<string>('');
    const [url, setUrl] = useState<string>('ws://localhost:8000/');

    const connectSocket = () => {
        if (url) {
            const newSocket = new WebSocket(url);
            if (newSocket === null) {
                setFeedBack('Error: Invalid URL');
                return;
            }
            setSocket(newSocket);
            newSocket.onopen = () => setFeedBack('Connected');
            newSocket.onerror = (error) => setFeedBack(`Error: ${error}`);
            newSocket.onclose = () => setFeedBack('Connection closed');
        }
    };

    return (
        <div className="min-h-1/2 flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Socket Connection</h2>
                </div>
                <div className="flex items-center justify-center bg-gray-50 py-2 px-4 sm:px-6 lg:px-8">
                    <input type="text" className="border-2 border-gray-300 bg-white h-10 px-5 pr-16 rounded-lg text-sm focus:outline-none"
                        placeholder="ws://localhost:8000/ws/chat/room/"
                        defaultValue={url}
                        onChange={(e) => setUrl(e.target.value)} />
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={connectSocket}>Connect</button>
                </div>
                <div className="flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
                        {feedBack === 'Connected' ?
                            <Comunicate WebSocket={socket} /> :
                            <div id="_connectionFeedback" className="text-center">
                                {feedBack}
                            </div>
                        }
                    </div>
                </div>
            </div>
        </div>
    );
}