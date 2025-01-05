import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
    CrosswordProvider,
    ThemeProvider,
    CrosswordGrid,
    DirectionClues,
} from '@jaredreisinger/react-crossword';
import './Board.css';

function Board() {
    const [data, setData] = useState({
        across: {},
        down: {},
    });

    const crosswordProvider = useRef(null);

    const [loading, setLoading] = useState(false);
    const [start, setStart] = useState(true);
    const [correct, setCorrect] = useState(false);

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

    const handleGenerate = () => {
        console.log("generate");
        setCorrect(false);
        setStart(false);
        setLoading(true);
        fetchData();
    };

    const handleCheck = () => {
        if (crosswordProvider.current) {
            const isCorrect = crosswordProvider.current.isCrosswordCorrect();
            if (isCorrect) {
                setCorrect(true);
                console.log('Crossword is correct!');
            }
        }
    };

    const handleClear = () => {
        setCorrect(false);
        if (crosswordProvider.current) {
            crosswordProvider.current.reset();
            console.log('Crossword cleared.');
        }
    };

    const handleGiveUp = () => {
        setCorrect(false);
        if (crosswordProvider.current) {
            crosswordProvider.current.fillAllAnswers();
            console.log('All answers filled.');
        }
    };
    
    if (loading) {
        return (
            <p>Loading...</p>
        );
    }
    if (start) {
        return (
            <button className="button" onClick={handleGenerate}>Generate</button>
        );
    }
    else {     
        return (
            <div style={{display: 'flex',  alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '2em'}}>
                {correct && <h1 className='correct-message'>Correct!</h1>}
                <ThemeProvider
                    theme={{
                    highlightBackground: '#f99',
                    focusBackground: '#f00',
                    }}
                >
                    <CrosswordProvider ref={crosswordProvider} data={data}>
                    <div style={{ display: 'flex', gap: '2em' }}>
                        <div style={{ width: '10em', display: 'flex', flexDirection: 'column', gap: '4em' }}>
                            <DirectionClues direction="across" />
                        </div>
                        <div style={{ width: '10em' }}>
                        <CrosswordGrid />
                        </div>
                        <div style={{ width: '10em', display: 'flex', flexDirection: 'column', gap: '4em' }}>
                            <DirectionClues direction="down" />
                        </div>
                    </div>
                    </CrosswordProvider>
                </ThemeProvider>
                <div style={{display: 'flex', gap: '2em'}}>
                    <button className="button" onClick={handleCheck}>Check</button>
                    <button className="button" onClick={handleClear}>Clear</button>
                    <button className="button" onClick={handleGiveUp}>Give Up</button>
                </div>
                <button className="button" onClick={handleGenerate}>Generate New Crossword</button>
            </div>
        );
    }
}
    
export default Board;
