<?php
header('Content-disposition: attachment; filename=resume.pdf');
header('Content-type: application/pdf');
readfile('static/resume.pdf');
?/>