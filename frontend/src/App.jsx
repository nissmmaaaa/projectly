import { useState } from "react";
import "./App.css";

function App() {
  const [backendMessage, setBackendMessage] = useState("");
  const [projectIdea, setProjectIdea] = useState("");
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false);

  const testBackend = async () => {
    const response = await fetch("http://127.0.0.1:8000/");
    const data = await response.json();
    setBackendMessage(data.message);
  };

  const discoverResources = async () => {
    if (!projectIdea.trim()) {
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        `http://127.0.0.1:8000/datasets?query=${encodeURIComponent(
          projectIdea
        )}`
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();
      setDatasets(data);

      console.log("Dataset results:", data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-mark">P</div>
          <span>Projectly</span>
        </div>

        <nav>
          <a className="nav-item active">Dashboard</a>
          <a className="nav-item">New Project</a>
          <a className="nav-item">My Projects</a>
          <a className="nav-item">Search History</a>
          <a className="nav-item">Saved Resources</a>
        </nav>

        <div className="sidebar-bottom">
          <a className="nav-item">Settings</a>

          <div className="profile">
            <div className="avatar">N</div>
            <div>
              <strong>Nisma</strong>
              <small>Student</small>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main">

        <button onClick={testBackend}>
          Test Backend
        </button>

        {backendMessage && <p>{backendMessage}</p>}

        <header className="topbar">
          <div>
            <p className="eyebrow">PROJECT DISCOVERY</p>
            <h1>Good afternoon, Nisma.</h1>
          </div>

          <button className="new-project-btn">
            + New Project
          </button>
        </header>

        {/* Hero */}
        <section className="hero-card">
          <div className="hero-content">
            <p className="hero-label">START SOMETHING NEW</p>

            <h2>
              What are you planning
              <br />
              to build?
            </h2>

            <p className="hero-description">
              Describe your project idea and discover datasets,
              papers, repositories and resources to build it.
            </p>

            <div className="project-input">
              <input
                type="text"
                placeholder="Describe your project idea..."
                value={projectIdea}
                onChange={(e) => setProjectIdea(e.target.value)}
              />

              <button
                type="button"
                onClick={discoverResources}
                disabled={loading}
              >
                {loading ? "Searching..." : "Discover Resources →"}
              </button>
            </div>

            <div className="examples">
              <span>Try an example:</span>

              <button
                type="button"
                onClick={() =>
                  setProjectIdea("Medical Image Classification")
                }
              >
                Medical Image Classification
              </button>

              <button
                type="button"
                onClick={() =>
                  setProjectIdea("Smart Agriculture")
                }
              >
                Smart Agriculture
              </button>

              <button
                type="button"
                onClick={() =>
                  setProjectIdea("Sentiment Analysis")
                }
              >
                Sentiment Analysis
              </button>
            </div>
          </div>
        </section>

        {/* Dataset Results */}
        {datasets.length > 0 && (
          <section className="section">
            <div className="section-header">
              <div>
                <p className="section-label">
                  DISCOVERED RESOURCES
                </p>

                <h3>Recommended Datasets</h3>
              </div>
            </div>

            <div className="resource-grid">
              {datasets.map((dataset, index) => (
                <div className="resource-card" key={dataset.id || index}>
                  <span className="resource-type dataset">
                    DATASET
                  </span>

                  <h4>{dataset.id}</h4>

                  <p>
                    {dataset.description ||
                      "No description available."}
                  </p>

                  <div className="resource-footer">
                    <span>{dataset.source}</span>

                    <strong>
                      {dataset.similarity_score
                        ? `${(
                            dataset.similarity_score * 100
                          ).toFixed(1)}% match`
                        : "Recommended"}
                    </strong>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Quick Stats */}
        <section className="stats">
          <div className="glass-card">
            <span>Projects</span>
            <strong>08</strong>
            <small>Created so far</small>
          </div>

          <div className="glass-card">
            <span>Resources</span>
            <strong>124</strong>
            <small>Saved resources</small>
          </div>

          <div className="glass-card">
            <span>Datasets</span>
            <strong>36</strong>
            <small>Discovered</small>
          </div>

          <div className="glass-card">
            <span>Projects analyzed</span>
            <strong>12</strong>
            <small>AI analysis</small>
          </div>
        </section>

        {/* Recent Projects */}
        <section className="section">
          <div className="section-header">
            <div>
              <p className="section-label">YOUR WORK</p>
              <h3>Recent Projects</h3>
            </div>

            <button className="text-btn">
              View all →
            </button>
          </div>

          <div className="project-grid">
            <div className="project-card">
              <div className="project-icon">01</div>

              <h4>Handwritten Answer Evaluation</h4>

              <p>
                AI-based handwritten answer sheet grading system.
              </p>

              <div className="tags">
                <span>Computer Vision</span>
                <span>OCR</span>
              </div>
            </div>

            <div className="project-card">
              <div className="project-icon">02</div>

              <h4>Smart Agriculture System</h4>

              <p>
                Machine learning system for crop monitoring.
              </p>

              <div className="tags">
                <span>Machine Learning</span>
                <span>IoT</span>
              </div>
            </div>

            <div className="project-card add-card">
              <div className="plus">+</div>

              <h4>Start a new project</h4>

              <p>
                Turn your idea into a complete project plan.
              </p>
            </div>
          </div>
        </section>

        {/* Recommended Resources */}
        <section className="section">
          <div className="section-header">
            <div>
              <p className="section-label">
                DISCOVERED FOR YOU
              </p>

              <h3>Recommended Resources</h3>
            </div>

            <button className="text-btn">
              View all →
            </button>
          </div>

          <div className="resource-grid">

            <div className="resource-card">
              <span className="resource-type dataset">
                DATASET
              </span>

              <h4>Handwritten Text Recognition Dataset</h4>

              <p>
                Image dataset suitable for handwritten text
                recognition and OCR projects.
              </p>

              <div className="resource-footer">
                <span>Hugging Face</span>
                <strong>94% match</strong>
              </div>
            </div>

            <div className="resource-card">
              <span className="resource-type paper">
                RESEARCH PAPER
              </span>

              <h4>Automated Answer Evaluation</h4>

              <p>
                Research on automated assessment using NLP
                and computer vision.
              </p>

              <div className="resource-footer">
                <span>Semantic Scholar</span>
                <strong>91% match</strong>
              </div>
            </div>

            <div className="resource-card">
              <span className="resource-type github">
                GITHUB
              </span>

              <h4>Automated Grading System</h4>

              <p>
                Open-source implementation for automated
                answer evaluation.
              </p>

              <div className="resource-footer">
                <span>GitHub</span>
                <strong>89% match</strong>
              </div>
            </div>

          </div>
        </section>

      </main>
    </div>
  );
}

export default App;