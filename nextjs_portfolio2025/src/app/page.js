import PortfolioGrid from "./portfolio/_components/PortfolioGrid";
import NavBar from "./portfolio/_components/NavBar";
import { nunito } from "./portfolio/_font-config/nunito-google-font";

export default function Home() {
  return (
    <main>
      <NavBar />
      <div className="container top-space-accomodate-navbar">
        <section className="has-text-centered" id="about">
          <div className="columns is-vcentered">
            <div className="column">
              <div className="content pb-5 mx-5">
                <h3 className="title is-3 mb-5">Well hello.</h3>
                <p className="subtitle is-4 mx-5">
                  I'm Patrick, a Business-minded NodeJS developer with
                  experience in Enterprise Application API Integration, Web
                  Application Development, and Business Consulting with
                  corporate and small business executives.
                </p>
              </div>
            </div>
            <div className="column">
              <img
                className="hero-background"
                src="cat-hero-image-bg.jpg"
                alt="Photo of Cat"
              />
            </div>
          </div>

          <div className="columns has-same-height">
            <div className="column">
              <div className="card">
                <div className="card-content">
                  <h3 className="title is-4">Profile</h3>
                  <div className="content">
                    Email: patrick.wm.meaney@gmail.com
                  </div>
                  <br />
                  <div className="buttons has-addons is-centered">
                    <a
                      href="https://www.github.com/pmeaney/"
                      className="button is-link"
                    >
                      Github
                    </a>
                    <a
                      href="https://www.gitlab.com/pmeaney/"
                      className="button is-link"
                    >
                      Gitlab
                    </a>
                    <a
                      href="https://www.linkedin.com/in/pmeaney/"
                      className="button is-link"
                    >
                      LinkedIn
                    </a>
                  </div>
                </div>
              </div>
            </div>
            <div className="column">
              <div className="card my-mobile-only-height-adjustment">
                <div className="card-content skills-content">
                  <h3 className="title is-4">Full Stack</h3>
                  <div className="content">
                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>
                              NodeJS / ExpressJS / General JavaScript:
                            </strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="90"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>

                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>ReactJS:</strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="70"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>

                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>React Native:</strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="50"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>
                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>
                              User Interface Design & Development:
                            </strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="60"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>
                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>
                              SQL/NoSQL Database Design &amp; Integration / REST
                              API
                            </strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="80"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>
                  </div>
                </div>
              </div>
            </div>
            <div className="column">
              <div className="card my-mobile-only-height-adjustment">
                <div className="card-content skills-content">
                  <h3 className="title is-4">DevOps & Data</h3>
                  <div className="content">
                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>
                              Linux & Nginx Secure Server Administration:
                            </strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="80"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>

                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>Docker & Other DevOps:</strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="65"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>

                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>AWS Cloud & Serverless Framework</strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="70"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>
                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>
                              Python &#x27A1; DataSci &amp; WebApp Frameworks
                            </strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="60"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>

                    <article className="media">
                      <div className="media-content">
                        <div className="content">
                          <p>
                            <strong>
                              Customized Application Integration / ETL / Data
                              Pipelines
                            </strong>
                            <br />
                            <progress
                              className="progress is-primary"
                              value="85"
                              max="100"
                            ></progress>
                          </p>
                        </div>
                      </div>
                    </article>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <br />
          <div className="container">
            <div className="tags custom-tags">
              <span className="tag is-light">Linux</span>
              <span className="tag is-light">NGINX</span>
              <span className="tag is-light">Node.js</span>
              <span className="tag is-light">Express.js</span>
              <span className="tag is-light">JavaScript</span>
              <span className="tag is-light">Python</span>
              <span className="tag is-light">R (statistics)</span>
              <span className="tag is-light">AWS Cloud</span>
              <span className="tag is-light">AWS Lambda</span>
              <span className="tag is-light">AWS DynamoDB</span>
              <span className="tag is-light">Serverless.com Framework</span>
              <span className="tag is-light">Infrastructure as Code</span>
              <span className="tag is-light">HTML5/CSS/SASS</span>
              <span className="tag is-light">Bulma</span>
              <span className="tag is-light">Bootstrap</span>
              <span className="tag is-light">Webpack</span>
              <span className="tag is-light">Git</span>
              <span className="tag is-light">Relational Database Design</span>
              <span className="tag is-light">SQL</span>
              <span className="tag is-light">NoSQL</span>
              <span className="tag is-light">Data pipelines / ETL</span>
              <span className="tag is-light">Data Visualization</span>
              <span className="tag is-light">Data Engineering</span>
              <span className="tag is-light">
                REST API Design & Development
              </span>
              <span className="tag is-light">Systems Analysis & Design</span>
              <span className="tag is-light">
                Consulting at crux of IT & Business
              </span>
            </div>
          </div>
        </section>

        {/* <section className={`hero ${nunito.className}`}>
          <div className="content">
            <h1 className="title is-2 has-text-centered">Blogs & Projects</h1>
            <SectionRecentUpdates />
          </div>
        </section> */}
        <br />
        <br />
        <PortfolioGrid />
        <section className={`hero ${nunito.className}`}>
          <p>SectionBackground</p>
        </section>
        <section id="services" className={`hero ${nunito.className}`}>
          <p>SectionServices</p>
        </section>
      </div>
    </main>
  );
}
