HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Amarnath CDJ</title><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="" />
<meta name="author" content="http://webthemez.com" />
<link rel="stylesheet" href="index.css" />
</head>
<body>
  <header class="header" role="banner" id="top">
    <div class="row">
      <nav class="nav" role="navigation">
        <ul class="nav__items">
          <li class="nav__item"><a href="#work" class="nav__link">Work</a></li>
          <li class="nav__item"><a href="#clients" class="nav__link">Clients</a></li>
          <li class="nav__item">
            <a href="#about" class="nav__link">About</a>
          </li>
          <li class="nav__item">
            <a href="#contact" class="nav__link">Contact</a>
          </li>
        </ul>
      </nav>
    </div>
    <div class="header__text-box row">
      <div class="header__text">
        <h1 class="heading-primary">
          <span>Amarnath CDJ</span>
        </h1>
        <p>A Web Developer based in Kerala, India.</p>
        <a href="#contact" class="btn btn--pink">Get in touch</a>
      </div>
    </div>
  </header>

  <main role="main">
    <section class="work" id="work">
      <div class="row">
        <h2>My Works</h2>
        <div class="work__boxes">
          <div class="work__box">
            <div class="work__text">
              <h3>RApi</h3>
              <p>
                A free multipurpose REST APi
              </p>
              <ul class="work__list">
                <li>Python</li>
                <li>HTML</li>
                <li>Golang</li>
                <li>Telethon</li>
              </ul>

              <div class="work__links">
                <a href="https://nisar.surge.sh" target="_blank" class="link__text">
                  Visit Site <span>&rarr;</span>
                </a>
                <a href="https://github.com/amarnathcjd" title="Visit My Github" target="_blank">
                  <img src="./images/github.svg" class="work__code" alt="GitHub">
                </a>
              </div>
            </div>
            <div class="work__image-box">
              <img src="./images/project-1.png" class="work__image" alt="Project 1" />
            </div>
          </div>

          <div class="work__box">
            <div class="work__text">
              <h3>Calculator</h3>
              <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Quod,
                eius.
              </p>
              <ul class="work__list">
                <li>React</li>
                <li>Next.js</li>
                <li>Node</li>
                <li>MongoDB</li>
              </ul>

              <div class="work__links">
                <a href="#" class="link__text">
                  Visit Site <span>&rarr;</span>
                </a>
                <a href="#">
                  <img src="./images/github.svg" class="work__code" title="View Source Code" alt="GitHub">
                </a>
              </div>
            </div>
            <div class="work__image-box">
              <img src="./images/project-2.png" class="work__image" alt="Project 1" />
            </div>
          </div>

          <div class="work__box">
            <div class="work__text">
              <h3>Notificator</h3>
              <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Quod,
                eius.
              </p>
              <ul class="work__list">
                <li>React</li>
                <li>Next.js</li>
                <li>Node</li>
                <li>MongoDB</li>
              </ul>

              <div class="work__links">
                <a href="#" class="link__text">
                  Visit Site <span>&rarr;</span>
                </a>
                <a href="#">
                  <img src="./images/github.svg" class="work__code" title="View Source Code" alt="GitHub">
                </a>
              </div>
            </div>
            <div class="work__image-box">
              <img src="./images/project-3.png" class="work__image" alt="Project 3" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ***** Clients ***** -->

    <section class="client" id="clients">
      <div class="row">
        <h2>Clients</h2>
        <div class="client__logos">
          <!-- Add logos of the clients or companies you'have worked with. -->
          <img src="./images/ronjones.png" class="client__logo" alt="Company 2" />
          <img src="./images/goldengrid.png" class="client__logo" alt="Company 3" />
          <img src="./images/bullseye.png" class="client__logo" alt="Company 1" />
          <img src="./images/mighty-furnitures.png" class="client__logo" alt="Company 1" />
          <img src="./images/fastlane.png" class="client__logo" alt="Company 3" />
          <img src="./images/chippy.png" class="client__logo" alt="Company 1" />
        </div>
      </div>
    </section>

    <!-- ***** About ***** -->

    <section class="about" id="about">
      <div class="row">
        <h2>About Me</h2>
        <div class="about__content">
          <div class="about__text">
            <!-- Replace the below paragraph with info about yourself -->
            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eos id
              nostrum illo harum blanditiis, tenetur eum suscipit cupiditate
              in vel, ex quam quidem quos mollitia labore aut sunt eius
              ratione molestiae fuga veniam facere similique voluptate.
            </p>
            <!-- Provide a link to your resume -->
            <a href="#" class="btn">My Resume</a>
          </div>

          <div class="about__photo-container">
            <!-- Add a nice photo of yourself -->
            <img class="about__photo" src="./images/syed-ali-hussnain.jpg" alt="" />
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- ***** Contact ***** -->

  <section class="contact" id="contact">
    <div class="row">
      <h2>Get in Touch</h2>
      <div class="contact__info">
        <p>
          Are you looking for a fast-performing and user-friendly website to
          represent your product or business? or looking for any kind of
          consultation? or want to ask questions? or have some advice for me
          or just want to say "Hi 👋" in any case feel free to Let me know. I
          will do my best to respond back. 😊 The quickest way to reach out to
          me is via an email.
        </p>
        <!-- Replace the email with yours -->
        <a href="mailto:you@example.com" class="btn">you@example.com</a>
      </div>
    </div>
  </section>

  <!-- ***** Footer ***** -->

  <footer role="contentinfo" class="footer">
    <div class="row">
      <!-- Update the links to point to your accounts -->
      <ul class="footer__social-links">
        <li class="footer__social-link-item">
          <a href="https://twitter.com/nisarhassan12/" title="Link to Twitter Profile">
            <img src="./images/twitter.svg" class="footer__social-image" alt="Twitter">
          </a>
        </li>
        <li class="footer__social-link-item">
          <a href="https://github.com/nisarhassan12/" title="Link to Github Profile">
            <img src="./images/github.svg" class="footer__social-image" alt="Github">
          </a>
        </li>
        <li class="footer__social-link-item">
          <a href="https://codepen.io/nisar_hassan" title="Link to Codepen Profile">
            <img src="./images/codepen.svg" class="footer__social-image" alt="Codepen">
          </a>
        </li>
        <li class="footer__social-link-item">
          <a href=https://www.linkedin.com/in/nisar-hassan-naqvi-413466199/">
            <img src="./images/linkedin.svg" title="Link to Linkedin Profile" class="footer__social-image" alt="Linkedin">
          </a>
        </li>
      </ul>

      <!-- If you give me some credit by keeping the below paragraph, will be huge for me 😊 Thanks. -->
      <p>
        &copy; 2020 - Template designed & developed by <a href="https://nisar.dev" class="link">Nisar</a>.
      </p>
      <div class="footer__github-buttons">
        <iframe
          src="https://ghbtns.com/github-btn.html?user=nisarhassan12&repo=portfolio-template&type=watch&count=true"
          frameborder="0" scrolling="0" width="170" height="20" title="Watch Portfolio Template on GitHub">
        </iframe>
      </div>
    </div>
  </footer>

  <a href="#top" class="back-to-top" title="Back to Top">
    <img src="./images/arrow-up.svg" alt="Back to Top" class="back-to-top__image"/>
  </a>
  <script src="./index.js"></script>
</body>

</html>
"""
