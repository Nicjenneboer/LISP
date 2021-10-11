(defun even (n) ( if (= n 0) (write "EVEN") (odd ( - n 1 ))  ))
(defun odd (n) ( if (= n 0) (write "ODD") (even ( - n 1 ))  ))

(even 111)
(even 112)