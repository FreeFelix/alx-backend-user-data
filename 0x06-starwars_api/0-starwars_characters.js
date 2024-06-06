#!/usr/bin/node

/**
 * A script to retrieve and print the names of characters from a specified
 * Star Wars film using the Star Wars API (SWAPI).
 *
 * Usage:
 *   ./script.js <film_id>
 *
 * <film_id>: The ID of the Star Wars film for which to retrieve character names.
 *
 * Example:
 *   ./script.js 1
 *   This will print the names of characters from the film with ID 1.
 *
 * This script uses the 'request' module to make HTTP requests to the SWAPI.
 * It handles asynchronous requests for character details using Promises.
 *
 * Author: Your Name
 * Date: YYYY-MM-DD
 */

const request = require('request');

// Get the film ID from the command line arguments
const filmId = process.argv[2];

// Construct the URL for the Star Wars API film endpoint
const url = `https://swapi-api.hbtn.io/api/films/${filmId}`;

// Make a request to the Star Wars API to get the film details
request(url, async (err, response, body) => {
  // Check for any errors in the request
  if (err) {
    console.log(err);
  }

  // Parse the response body to get the list of character URLs
  const characters = JSON.parse(body).characters;

  // Iterate over each character URL
  for (const characterId of characters) {
    // Use a Promise to handle the asynchronous request for each character
    await new Promise((resolve, reject) => {
      // Make a request to get the character details
      request(characterId, (err, response, body) => {
        // Check for any errors in the request
        if (err) {
          reject(err);
        }
        // Parse and print the character name
        console.log(JSON.parse(body).name);
        resolve();
      });
    });
  }
});
