import "./App.css";

function App() {
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
                placeholder="e.g. AI system for handwritten answer sheet grading"
              />

              <button>Discover Resources →</button>
            </div>

            <div className="examples">
              <span>Try an example:</span>
              <button>Medical Image Classification</button>
              <button>Smart Agriculture</button>
              <button>Sentiment Analysis</button>
            </div>
          </div>
        </section>

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

            <button className="text-btn">View all →</button>
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
              <p>Turn your idea into a complete project plan.</p>
            </div>
          </div>
        </section>

        {/* Recommended Resources */}
        <section className="section">
          <div className="section-header">
            <div>
              <p className="section-label">DISCOVERED FOR YOU</p>
              <h3>Recommended Resources</h3>
            </div>

            <button className="text-btn">View all →</button>
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