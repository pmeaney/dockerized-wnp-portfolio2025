"use client";

import { nunitoBold, nunitoSemiBold } from "../_font-config/nunito-google-font";
import Link from "next/link";
import { useEffect } from "react";

export default function NavBar() {
  useEffect(() => {
    // Function to initialize the navbar functionality
    const initializeNavbar = () => {
      // Select all elements with the "navbar-burger" class
      // These are the hamburger buttons used to toggle the menu on smaller screens
      const navbarBurgers = document.querySelectorAll(".navbar-burger");

      // Select all elements inside the menu with the "navbar-item" class
      // These are the individual menu items that the user can click on
      const navbarItems = document.querySelectorAll(
        ".navbar-menu .navbar-item"
      );

      // Function to close the navbar
      // This removes the "is-active" class from the hamburger button and the menu, collapsing it
      const closeNavbar = () => {
        // Remove "is-active" class from all navbar-burger elements
        navbarBurgers.forEach((burger) => burger.classList.remove("is-active"));

        // Get the target menu ID from the first navbar-burger's "data-target" attribute
        const targetId = navbarBurgers[0]?.dataset.target;

        // Find the menu element by ID and remove the "is-active" class to hide it
        const target = document.getElementById(targetId);
        target?.classList.remove("is-active");
      };

      // Add click event listeners to all navbar-burger elements ...test
      navbarBurgers.forEach((burger) => {
        burger.addEventListener("click", () => {
          // Get the ID of the target menu from the "data-target" attribute
          const targetId = burger.dataset.target;

          // Find the menu element by ID
          const target = document.getElementById(targetId);

          // Toggle the "is-active" class on both the burger and the menu
          // This expands or collapses the menu
          burger.classList.toggle("is-active");
          target.classList.toggle("is-active");
        });
      });

      // Add click event listeners to all menu items
      navbarItems.forEach((item) => {
        // When a menu item is clicked, call the closeNavbar function to collapse the menu
        item.addEventListener("click", closeNavbar);
      });
    };

    // Check if the DOM is still loading
    // If yes, wait for the "DOMContentLoaded" event before running the initializer
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initializeNavbar);
    } else {
      // If the DOM is already loaded, run the initializer immediately
      initializeNavbar();
    }

    // Cleanup function to remove event listeners when the component unmounts
    return () => {
      // Remove the "DOMContentLoaded" event listener (if it was added)
      document.removeEventListener("DOMContentLoaded", initializeNavbar);
    };
  }, []);

  return (
    <nav
      className="navbar is-fixed-top"
      role="navigation"
      aria-label="main navigation"
    >
      <div className="navbar-brand">
        <section className={`hero`}>
          <div className="hero-body is-flex is-vcentered is-justify-content-space-between py-3 m-0">
            <div>
              <h1
                className={`p-0 m-0 my-title title is-4 ${nunitoBold.className}`}
              >
                <Link href={`${process.env.MAIN_SITE_BASE_URL}`}>
                  Patrick Meaney
                </Link>
              </h1>
              <h2
                className={`p-0 m-0 subtitle is-5 ${nunitoSemiBold.className}`}
              >
                Web App Software Engineer
              </h2>
            </div>
          </div>
        </section>

        <a
          role="button"
          className="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbarBasicExample"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" className="navbar-menu">
        <div className="navbar-start">
          <Link className="navbar-item" href={`#portfolio`}>
            Portfolio
          </Link>

          {/* <a className="navbar-item">Services</a> */}
          <Link className="navbar-item" href={`#services`}>
            Services
          </Link>

          {/* <div className="navbar-item has-dropdown is-hoverable">
            <a className="navbar-link">More</a>

            <div className="navbar-dropdown">
              <a className="navbar-item">About</a>
              <a className="navbar-item is-selected">Jobs</a>
              <a className="navbar-item">Contact</a>
              <a className="navbar-item">Report an issue</a>
            </div>
          </div> */}
        </div>

        {/* <div className="navbar-end">
          <div className="navbar-item">
            <div className="buttons">
              <a className="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a className="button is-light">Log in</a>
            </div>
          </div>
        </div> */}
      </div>
    </nav>
  );
}
