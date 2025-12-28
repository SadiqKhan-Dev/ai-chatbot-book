import React, {useState, useEffect} from 'react';
import styles from './styles.module.css';

const documents = [
  '/docs/physical-ai-robotics-course/01-introduction-to-physical-ai.md',
  '/docs/physical-ai-robotics-course/02-sensors-and-perception.md',
  '/docs/physical-ai-robotics-course/03-actuators-and-control.md',
  '/docs/physical-ai-robotics-course/04-kinematics-and-dynamics.md',
  '/docs/physical-ai-robotics-course/05-locomotion.md',
  '/docs/physical-ai-robotics-course/06-manipulation.md',
  '/docs/physical-ai-robotics-course/07-planning-and-navigation.md',
  '/docs/physical-ai-robotics-course/08-machine-learning-for-robotics.md',
  '/docs/physical-ai-robotics-course/09-human-robot-interaction.md',
  '/docs/physical-ai-robotics-course/savory-aiding-learning-in-physical-ai-and-robotics-course.md'
];

export default function FloatingAiAgent() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [allDocuments, setAllDocuments] = useState([]);

  useEffect(() => {
    if (isOpen && allDocuments.length === 0) {
      Promise.all(
        documents.map((url) =>
          fetch(url).then((res) => res.text())
        )
      ).then((texts) => {
        setAllDocuments(texts);
      });
    }
  }, [isOpen]);

  const search = (query) => {
    const queryWords = query.toLowerCase().split(/\s+/);
    let bestDoc = '';
    let maxScore = 0;

    allDocuments.forEach((doc) => {
      const score = queryWords.reduce((acc, word) => {
        return acc + (doc.toLowerCase().includes(word) ? 1 : 0);
      }, 0);

      if (score > maxScore) {
        maxScore = score;
        bestDoc = doc;
      }
    });

    return bestDoc;
  };

  const handleSendMessage = () => {
    if (input.trim() === '') {
      return;
    }

    const newMessages = [...messages, {text: input, sender: 'user'}];
    setMessages(newMessages);
    setInput('');

    setTimeout(() => {
      const relevantDoc = search(input);
      const geminiResponsePrefix = "Based on the book, here's an answer to your question powered by Gemini 2.5 Flash:\n\n";
      const response = relevantDoc
        ? `${geminiResponsePrefix}${relevantDoc.slice(0, 500)}...`
        : `${geminiResponsePrefix}I couldn't find any relevant information in the book for your query.`;

      setMessages([
        ...newMessages,
        {text: response, sender: 'ai'},
      ]);
    }, 1000);
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };
  
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <button className={styles.chatButton} onClick={toggleChat}>
        🤖
      </button>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h2>AI Assistant (Powered by Gemini 2.5 Flash)</h2>
            <button onClick={toggleChat}>X</button>
          </div>
          <div className={styles.chatMessages}>
            {messages.map((message, index) => (
              <div key={index} className={`${styles.message} ${styles[message.sender]}`}>
                <pre style={{fontFamily: 'inherit', whiteSpace: 'pre-wrap'}}>{message.text}</pre>
              </div>
            ))}
          </div>
          <div className={styles.chatInput}>
            <input
              type="text"
              value={input}
              onChange={handleInputChange}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
