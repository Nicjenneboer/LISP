(defun even (n) ( if (= n 0) "EVEN" (odd ( - n 1 ))  ))
(defun odd (n) ( if (= n 0) "ODD" (even ( - n 1 ))  ))

(write(even 111))
(write(even 112))

(defun factorial (n) (if (= n 0) 1 (* n (factorial (- n 1))))  )

(write(factorial 6))
(write(factorial 7))
(write(factorial 8))
