import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';

export default function App() {
    const [courseTitle, setCourseTitle] = useState(''); // ✅ Added this state
    const [moduleTitle, setModuleTitle] = useState('');
    const [questions, setQuestions] = useState([]);
    const [quiz_sessionID, setQuiz_sessionID] = useState('');
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [showScore, setShowScore] = useState(false);
    const [score, setScore] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [isCorrectAnswer, setIsCorrectAnswer] = useState(null);
    const [showExplanation, setShowExplanation] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('https://amazoninstructor.info/json/questions.json')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setCourseTitle(data.courseTitle); // ✅ Now works
                setModuleTitle(data.moduleTitle);
                setQuestions(data.questionSet);
                setQuiz_sessionID(data.quiz_sessionID);
            })
            .catch((error) => setError(error.message));
    }, []);

    const handleAnswerOptionClick = (isCorrect, index) => {
        setSelectedAnswer(index);
        setIsCorrectAnswer(isCorrect);
        setShowExplanation(true);
        if (isCorrect) setScore(score + 1);
    };

    const handleNextQuestion = () => {
        setSelectedAnswer(null);
        setIsCorrectAnswer(null);
        setShowExplanation(false);
        if (currentQuestion < questions.length - 1) setCurrentQuestion(currentQuestion + 1);
    };

    const handlePreviousQuestion = () => {
        setSelectedAnswer(null);
        setIsCorrectAnswer(null);
        setShowExplanation(false);
        if (currentQuestion > 0) setCurrentQuestion(currentQuestion - 1);
    };

    const handleEndQuiz = () => {
        setShowScore(true);
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className='container-fully'>
            <div className='app'>
                {questions.length > 0 ? (
                    showScore ? (
                        <div className='score-section'>
                            <h5>{quiz_sessionID}</h5>
                            <table>
                                <h3>{moduleTitle}</h3>
                                You scored {score} out of {questions.length}
                            </table>
                        </div>
                    ) : (
                        <>
                            <div className='header-section'>
                                <h3>{courseTitle}</h3>
                                <h4>{moduleTitle}</h4>
                            </div>
                            <div className='question-section'>
                                <div className='question-count'>
                                    <span>Question {currentQuestion + 1}</span>/{questions.length}
                                </div>
                                <div className='question-text'>{questions[currentQuestion].questionText}</div>
                            </div>
                            <div className='answer-section'>
                                {questions[currentQuestion].answerOptions.map((answerOption, index) => (
                                    <button
                                        key={index}
                                        className={
                                            selectedAnswer === index
                                                ? isCorrectAnswer
                                                    ? 'correct'
                                                    : 'incorrect'
                                                : ''
                                        }
                                        onClick={() => handleAnswerOptionClick(answerOption.isCorrect, index)}
                                        disabled={selectedAnswer !== null}
                                    >
                                        {answerOption.answerText}
                                    </button>
                                ))}
                            </div>
                            {showExplanation && (
                                <div className='explanation-section'>
                                    <ReactMarkdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]}>
                                        {questions[currentQuestion].explanation}
                                    </ReactMarkdown>
                                </div>
                            )}
                            <div className='navigation-buttons'>
                                <button onClick={handlePreviousQuestion} disabled={currentQuestion === 0}>
                                    Previous
                                </button>
                                {currentQuestion === questions.length - 1 ? (
                                    <button onClick={handleEndQuiz}>End</button>
                                ) : (
                                    <button
                                        onClick={handleNextQuestion}
                                        disabled={currentQuestion === questions.length - 1}
                                    >
                                        Next
                                    </button>
                                )}
                            </div>
                        </>
                    )
                ) : (
                    <div>Loading...</div>
                )}
            </div>
        </div>
    );
}
