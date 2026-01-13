import React, { useState } from "react";
import axios from "axios";

function FetchDataReddit() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const getData = async () => {
        try {
            setLoading(true);
            setError(null);

            const res = await axios.get("http://127.0.0.1:5000/data");

            const cleanPosts = res.data.data.children.map(item => ({
                id: item.data.id,
                title: item.data.title,
                author: item.data.author,
                upvotes: item.data.ups
            }));

            setPosts(cleanPosts);
        } catch (err) {
            setError("Failed to load posts");
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h2>Reddit Posts</h2>
            <button onClick={getData}>Fetch Posts</button>

            <ul>
                {posts.map(post => (
                    <li key={post.id}>
                        <h3>{post.title}</h3>
                        <p>By {post.author}</p>
                        <p>⬆ {post.upvotes}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default FetchDataReddit;
