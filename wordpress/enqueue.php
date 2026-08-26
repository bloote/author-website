<?php
/**
 * AuthorWings — Author Websites page assets.
 *
 * Drop this into the GeneratePress child theme's functions.php (or save it as
 * inc/author-websites.php and require it from there). The stylesheet and
 * script load only on the Author Websites page, so nothing else on the site
 * pays for them.
 *
 * Expected layout inside the child theme:
 *   generatepress_child/
 *     assets/css/author-websites.css
 *     assets/js/author-websites.js
 *
 * Images live in the uploads directory instead — see the note in
 * wordpress/author-websites-content.html.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Is the current request the Author Websites page?
 *
 * Matches by slug so the page can be re-created without touching code.
 */
function authorwings_is_websites_page() {
	return is_page( 'author-websites' );
}

/**
 * Register and enqueue the page's stylesheet and script.
 */
function authorwings_websites_assets() {
	if ( ! authorwings_is_websites_page() ) {
		return;
	}

	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	$css = '/assets/css/author-websites.css';
	$js  = '/assets/js/author-websites.js';

	// filemtime() as the version busts the cache on every deploy.
	wp_enqueue_style(
		'authorwings-websites',
		$uri . $css,
		array(),
		file_exists( $dir . $css ) ? filemtime( $dir . $css ) : null
	);

	wp_enqueue_script(
		'authorwings-websites',
		$uri . $js,
		array(),
		file_exists( $dir . $js ) ? filemtime( $dir . $js ) : null,
		true // in the footer; the script is defer-safe either way.
	);
}
add_action( 'wp_enqueue_scripts', 'authorwings_websites_assets' );

/**
 * The theme already serves Lora and Inter, so assets/css/fonts.css and
 * assets/fonts/ from this repo are only needed for the standalone preview.
 * If you ever move the page to a theme that does not load them, enqueue the
 * font stylesheet here too:
 *
 *   wp_enqueue_style( 'authorwings-fonts', $uri . '/assets/css/fonts.css' );
 */
