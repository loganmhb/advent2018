(ns adventofcode.core
  (:require [clojure.java.io :as io]
            [clojure.string :as string]))

(defn day1-part1 []
  (let [input (slurp (io/resource "day1_input"))]
    (reduce + (map #(Integer/parseInt %) (string/split input #"\n")))))

(defn day1-part2 []
  (let [input (slurp (io/resource "day1_input"))]
    (loop [freq 0
           seen #{}
           changes (cycle (map #(Integer/parseInt %)
                               (string/split input #"\n")))]
      (let [next-freq (+ freq (first changes))]
        (if (seen next-freq)
          next-freq
          (recur next-freq
                 (conj seen next-freq)
                 (rest changes)))))))

(defn day2-part1 []
  (let [input (string/split (slurp (io/resource "day2_input")) #"\n")
        freqs (map (comp set vals frequencies) input)
        twos (filter #(contains? % 2) freqs)
        threes (filter #(contains? % 3) freqs)]
    (* (count twos) (count threes))))

(defn diff-by-one-char? [a b]
  (loop [a a
         b b
         found-diff? false]
    (if (or (nil? (first a)) (nil? (first b)))
      found-diff?
      (if (= (first a) (first b))
        (recur (rest a) (rest b) found-diff?)
        (if found-diff?
          false
          (recur (rest a) (rest b) true))))))

(defn day2-part2 []
  (let [input (string/split (slurp (io/resource "day2_input")) #"\n")]
    (filter seq (map (fn [id] (filter #(diff-by-one-char? id %) input)) input))
    ))

(day2-part1)

(defn parse-claims []
  (let [input (string/split (slurp (io/resource "day3_input")) #"\n")]
    (map (fn [c]
           (let [[_ id x y width height]
                 (re-find #"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)" c)]
             {:id id :x (Integer/parseInt x) :y (Integer/parseInt y) :width (Integer/parseInt width) :height (Integer/parseInt height)}))
         input)))

(defn claim-counts-by-square [claims]
  (frequencies (for [claim claims
                     x (range (:x claim) (+ (:x claim) (:width claim)))
                     y (range (:y claim) (+ (:y claim) (:height claim)))]
                 [x y])))

(defn day3-part1 []
  (let [claims (parse-claims)]
    (count (filter (fn [[coord freq]] (> freq 1)) (claim-counts-by-square claims)))))

(day3-part1)

(defn day3-part2 []
  (let [claims (parse-claims)
        squares-claimed (claim-counts-by-square claims)]
    (first (filter (fn [claim]
                     (println claim)
                     (println "claim counts by square" (squares-claimed [1 1]))
                     (every? (fn [square] (= (squares-claimed square) 1))
                             (for [x (range (:x claim) (+ (:x claim) (:width claim)))
                                   y (range (:y claim) (+ (:y claim) (:height claim)))]
                               [x y])))
                   claims))))

(day3-part2)

(defn parse-guard-times []
  (let [input (string/split (slurp (io/resource "day4_input")) #"\n")]
    (reduce (fn [stats line]
              (if (re-match #"Guard #(\d+) begins shift")
                ;; discard the day, we don't care
                (assoc stats )
                ))
            {:current-guard nil
             :sleep-times {}}
            input)))

(defn day4-part1 []
  )
(defn foo
  "I don't do a whole lot."
  [x]
  (println x "Hello, World!"))

(defn sum-node-meta [s]
  (let [[num-children num-meta & remaining] s]
    (let [s (reduce ())])
    (reduce +
            (take num-meta s)
            (reduce ))))

(defn read-node [s]
  (let [[num-children num-meta & remaining] s
        [children remaining] (loop [children []
                                    remaining remaining
                                    num-children-read 0]
                               (if (= num-children-read num-children)
                                 [children remaining]
                                 (let [[child next-remaining] (read-node remaining)]
                                   (recur (conj children child)
                                          next-remaining
                                          (inc num-children-read)))))
        metadata (take num-meta remaining)]
    [{:children children :metadata metadata} (drop num-meta remaining)]))

(defn day8-part1 []
  (let [input (map #(Integer/parseInt %) (string/split (slurp (io/resource "day8_input")) #" "))]
    (clojure.walk/postwalk (fn [tree]
                             (if (:metadata tree)
                               (apply + (concat (:metadata tree) (:children tree)))
                               tree))
                           (read-node input))))

(day8-part1)
