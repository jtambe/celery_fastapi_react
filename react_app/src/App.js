import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [numberA, setNumberA] = useState('');
  const [numberB, setNumberB] = useState('');
  const [taskId, setTaskId] = useState('');
  const [taskStatus, setTaskStatus] = useState(null);
  const [taskResult, setTaskResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL;

  // Fetch all tasks
  useEffect(() => {
    fetch(`${API_URL}/api/v0/all_tasks`)
      .then(res => res.json())
      .then(data => setTasks(data));
  }, [API_URL]);

  // Create a new task (process)
  const handleCreateTask = async (endpoint) => {
    setLoading(true);
    await fetch(`${API_URL}/api/v0/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ numberA: Number(numberA), numberB: Number(numberB) })
    });
    setLoading(false);
    window.location.reload(); // Refresh to show new task
  };

  // Get status/result of a task
  const handleGetTaskInfo = async (type) => {
    setLoading(true);
    const res = await fetch(`${API_URL}/api/v0/${type}?task_id=${taskId}`);
    const data = await res.json();
    if (type === 'task_status') setTaskStatus(data);
    else setTaskResult(data);
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Task Manager</h1>
      <h2>Create Task</h2>
      <input placeholder="Number A" value={numberA} onChange={e => setNumberA(e.target.value)} />
      <input placeholder="Number B" value={numberB} onChange={e => setNumberB(e.target.value)} />
      <button onClick={() => handleCreateTask('process')} disabled={loading}>Create Process Task</button>
      <button onClick={() => handleCreateTask('process2')} disabled={loading}>Create Process2 Task</button>

      <h2>All Tasks</h2>
      <ul>
        {tasks.map(task => (
          <li key={task.task_id}>
            ID: {task.task_id} | Status: {task.status} | Result: {task.result?.toString()}
          </li>
        ))}
      </ul>


      <h2>Get Task Status/Result</h2>
      <input placeholder="Task ID" style={{ width: '300px' }} value={taskId} onChange={e => setTaskId(e.target.value)} />
      <button onClick={() => handleGetTaskInfo('task_status')} disabled={loading}>Get Status</button>
      <button onClick={() => handleGetTaskInfo('task_result')} disabled={loading}>Get Result</button>
      {taskStatus && (
        <div>
          <h3>Status</h3>
          <pre>{JSON.stringify(taskStatus, null, 2)}</pre>
        </div>
      )}
      {taskResult && (
        <div>
          <h3>Result</h3>
          <pre>{JSON.stringify(taskResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
