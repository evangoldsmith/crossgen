import React, { useState, useEffect } from "react";
import Crossword from '@jaredreisinger/react-crossword';

function Board() {
    const [data, setData] = useState({
        across: {},
        down: {},
      });
    
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("fetching");
                const response = await fetch("/generate");
                const jsonData = await response.json();
                
                setData({
                    across: jsonData.across,
                    down: jsonData.down,
                });
                setLoading(false);
            } catch (error) {
                console.error("Error fetching crossword:", error);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <p>Loading...</p>
        );
    }
    
    return (
        <div style={{ width: '25em', display: 'flex' }}>
            <Crossword data={data} />
        </div>
    );
}
    
export default Board;
